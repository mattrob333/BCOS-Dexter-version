"""
Truth Engine for BCOS Multi-Source Verification.

The Truth Engine is responsible for:
1. Cross-referencing facts across multiple data sources
2. Assigning confidence scores based on source agreement
3. Detecting and resolving conflicts
4. Ensuring 100% source attribution
5. Preventing hallucinations by requiring evidence

Core principle: Every fact must be verifiable in at least one source.
If not found in sources, explicitly mark as unverified.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import re
from difflib import SequenceMatcher

from core.models import (
    VerifiedFact,
    Source,
    SourceType,
    Conflict,
    VerifiedDataset
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TruthEngine:
    """
    Multi-source verification engine.

    Validates claims across multiple sources and assigns confidence scores
    based on source agreement, recency, and reliability.
    """

    def __init__(self, min_confidence: float = 0.2):
        """
        Initialize Truth Engine.

        Args:
            min_confidence: Minimum confidence threshold for accepting facts (0.0-1.0)
                          Default 0.2 for permissive Phase 1 research (user-editable)
        """
        self.min_confidence = min_confidence

        # Source reliability weights (can be configured per source)
        self.source_reliability = {
            SourceType.PRIMARY: 1.0,  # Official company sources
            SourceType.SECONDARY: 0.8,  # News, research reports
            SourceType.TERTIARY: 0.6,  # Third-party databases
            SourceType.VERIFICATION: 0.9,  # Fact-checking services
        }

    def verify_claim(
        self,
        claim: str,
        value: Any,
        sources_data: List[Dict[str, Any]]
    ) -> VerifiedFact:
        """
        Verify a single claim across multiple sources.

        Args:
            claim: The fact being claimed (e.g., "Annual Revenue")
            value: The claimed value (e.g., "$1 trillion")
            sources_data: List of source data dictionaries

        Returns:
            VerifiedFact with confidence score and source attribution
        """
        logger.debug(f"Verifying claim: {claim}")

        sources = []
        supporting_sources = []
        conflicting_values = []

        # Extract sources and check for support
        for source_data in sources_data:
            source = self._create_source(source_data)
            sources.append(source)

            # Check if this source supports the claim
            if self._source_supports_claim(source_data, claim, value):
                supporting_sources.append(source)
            else:
                # Check for conflicts
                alt_value = self._extract_value_from_source(source_data, claim)
                if alt_value and alt_value != value:
                    conflicting_values.append((alt_value, source))

        # Calculate confidence based on source agreement
        confidence = self._calculate_confidence(
            supporting_sources,
            len(sources),
            conflicting_values
        )

        # Detect conflicts
        conflicts = []
        if conflicting_values:
            conflict = Conflict(
                claim=claim,
                conflicting_values=[value] + [v for v, _ in conflicting_values],
                sources=[s for _, s in conflicting_values],
                severity=self._assess_conflict_severity(conflicting_values),
                resolution=None
            )
            conflicts.append(conflict)

        # Determine if verified
        # PERMISSIVE MODE: Accept data even with conflicts (Phase 1 is user-editable)
        # We include conflicting data and let users decide - transparency over strictness
        verified = (
            len(supporting_sources) > 0 and
            confidence >= self.min_confidence
            # Removed: len(conflicts) == 0  - conflicts no longer block verification
        )

        return VerifiedFact(
            claim=claim,
            value=value,
            verified=verified,
            confidence=confidence,
            sources=supporting_sources if supporting_sources else sources,
            conflicts=conflicts,
            notes=self._generate_verification_notes(
                supporting_sources, conflicting_values
            )
        )

    def cross_reference(
        self,
        datasets: List[Dict[str, Any]],
        entity_name: str,
        entity_type: str = "company"
    ) -> VerifiedDataset:
        """
        Cross-reference data across multiple source datasets.

        Args:
            datasets: List of data dictionaries from different sources
            entity_name: Name of the entity (e.g., company name)
            entity_type: Type of entity

        Returns:
            VerifiedDataset with all verified facts
        """
        logger.info(f"Cross-referencing data for {entity_name}")

        # Extract all unique claims across datasets
        all_claims = self._extract_all_claims(datasets)

        # Verify each claim
        verified_facts = []
        for claim_key, claim_info in all_claims.items():
            verified_fact = self.verify_claim(
                claim=claim_info['claim'],
                value=claim_info['value'],
                sources_data=claim_info['sources']
            )
            verified_facts.append(verified_fact)

        # Create verified dataset
        dataset = VerifiedDataset.from_facts(
            entity_name=entity_name,
            entity_type=entity_type,
            facts=verified_facts
        )

        logger.info(
            f"Verification complete: {dataset.verified_count} verified, "
            f"{dataset.unverified_count} unverified, "
            f"{dataset.conflict_count} conflicts"
        )

        return dataset

    def _create_source(self, source_data: Dict[str, Any]) -> Source:
        """Create Source object from data dictionary."""
        source_type_str = source_data.get('source_type', 'secondary')
        try:
            source_type = SourceType(source_type_str.lower())
        except ValueError:
            source_type = SourceType.SECONDARY

        return Source(
            url=source_data.get('url', 'unknown'),
            source_type=source_type,
            source_name=source_data.get('source_name', 'Unknown Source'),
            date_accessed=datetime.now(),
            date_published=source_data.get('date_published'),
            reliability_score=source_data.get('reliability_score',
                                             self.source_reliability[source_type])
        )

    def _source_supports_claim(
        self,
        source_data: Dict[str, Any],
        claim: str,
        value: Any
    ) -> bool:
        """Check if source supports the claimed value."""
        # Extract data from source
        source_content = source_data.get('data', {})

        # Try to find claim in source data
        claim_key = self._normalize_key(claim)

        # Check direct match
        if claim_key in source_content:
            source_value = source_content[claim_key]
            return self._values_match(value, source_value)

        # Check fuzzy match
        for key, val in source_content.items():
            if self._keys_similar(claim_key, key):
                if self._values_match(value, val):
                    return True

        return False

    def _extract_value_from_source(
        self,
        source_data: Dict[str, Any],
        claim: str
    ) -> Optional[Any]:
        """Extract value for claim from source, even if different."""
        source_content = source_data.get('data', {})
        claim_key = self._normalize_key(claim)

        # Check direct match
        if claim_key in source_content:
            return source_content[claim_key]

        # Check fuzzy match
        for key, val in source_content.items():
            if self._keys_similar(claim_key, key):
                return val

        return None

    def _calculate_confidence(
        self,
        supporting_sources: List[Source],
        total_sources: int,
        conflicts: List[Tuple[Any, Source]]
    ) -> float:
        """
        Calculate confidence score based on source agreement.

        Factors:
        - Number of supporting sources
        - Source reliability
        - Recency
        - Conflicts
        """
        if not supporting_sources:
            return 0.0

        # Base confidence from source agreement
        agreement_ratio = len(supporting_sources) / max(total_sources, 1)
        base_confidence = agreement_ratio

        # Weight by source reliability
        reliability_scores = [s.reliability_score for s in supporting_sources]
        avg_reliability = sum(reliability_scores) / len(reliability_scores)
        weighted_confidence = base_confidence * avg_reliability

        # Bonus for primary sources
        primary_count = sum(
            1 for s in supporting_sources if s.source_type == SourceType.PRIMARY
        )
        if primary_count > 0:
            weighted_confidence *= 1.1  # 10% boost for primary sources

        # Reduced penalty for conflicts (Phase 1 permissive mode)
        # Small penalty to prefer agreed-upon facts, but don't exclude conflicting data
        if conflicts:
            conflict_penalty = len(conflicts) * 0.02  # 2% per conflict (was 10%)
            weighted_confidence -= conflict_penalty

        # Bonus for multiple sources
        if len(supporting_sources) >= 3:
            weighted_confidence *= 1.05  # 5% boost for 3+ sources

        # Clamp to 0.0-1.0 range
        return max(0.0, min(1.0, weighted_confidence))

    def _extract_all_claims(
        self,
        datasets: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Extract all unique claims across datasets.

        Returns dict mapping claim_key -> {claim, value, sources}

        Intelligently merges values by preferring real data over "Unknown" or empty values.
        """
        claims = {}

        for dataset in datasets:
            data = dataset.get('data', {})

            for key, value in data.items():
                claim_key = self._normalize_key(key)

                if claim_key not in claims:
                    claims[claim_key] = {
                        'claim': key,
                        'value': value,
                        'sources': []
                    }
                else:
                    # Intelligently merge values - prefer data over "Unknown"
                    existing_value = claims[claim_key]['value']
                    new_value = value

                    # If new value is better than existing, update it
                    if self._is_better_value(new_value, existing_value):
                        claims[claim_key]['value'] = new_value

                claims[claim_key]['sources'].append(dataset)

        return claims

    def _is_better_value(self, new_value: Any, existing_value: Any) -> bool:
        """
        Determine if new_value is better than existing_value.

        Prefers actual data over "Unknown", empty strings, or empty collections.
        For nested dictionaries (like key_facts), merges intelligently.
        """
        # If existing is None or empty string, new is better
        if existing_value is None or existing_value == "":
            return new_value is not None and new_value != ""

        # If both are dicts (e.g., key_facts), merge intelligently
        if isinstance(existing_value, dict) and isinstance(new_value, dict):
            # Check if new_value has more real data than existing
            existing_real_count = sum(1 for v in existing_value.values()
                                     if v and v != "Unknown" and v != "")
            new_real_count = sum(1 for v in new_value.values()
                                if v and v != "Unknown" and v != "")

            # If new has more real data, it's better
            if new_real_count > existing_real_count:
                return True

            # If new has same or fewer, merge them (prefer non-Unknown values)
            if new_real_count >= existing_real_count:
                merged = existing_value.copy()
                for k, v in new_value.items():
                    if v and v != "Unknown" and v != "":
                        merged[k] = v
                # Update the existing value in place by returning False
                # but modifying existing_value (which is a reference)
                existing_value.update(merged)
            return False

        # For strings, prefer non-"Unknown" values
        if isinstance(existing_value, str) and isinstance(new_value, str):
            if existing_value.lower() == "unknown" and new_value.lower() != "unknown":
                return True
            if existing_value == "" and new_value != "":
                return True

        # For lists, prefer non-empty
        if isinstance(existing_value, list) and isinstance(new_value, list):
            if len(existing_value) == 0 and len(new_value) > 0:
                return True

        # Default: keep existing value
        return False

    def _normalize_key(self, key: str) -> str:
        """Normalize key for comparison."""
        # Convert to lowercase, remove special chars, collapse whitespace
        normalized = re.sub(r'[^a-z0-9\s]', '', key.lower())
        normalized = re.sub(r'\s+', '_', normalized.strip())
        return normalized

    def _keys_similar(self, key1: str, key2: str, threshold: float = 0.8) -> bool:
        """Check if two keys are similar using fuzzy matching."""
        similarity = SequenceMatcher(None, key1, key2).ratio()
        return similarity >= threshold

    def _values_match(self, val1: Any, val2: Any, threshold: float = 0.9) -> bool:
        """Check if two values match (with fuzzy matching for strings)."""
        # Exact match
        if val1 == val2:
            return True

        # Type mismatch
        if type(val1) != type(val2):
            # Try string comparison
            return self._values_match(str(val1), str(val2), threshold)

        # String fuzzy matching
        if isinstance(val1, str) and isinstance(val2, str):
            similarity = SequenceMatcher(None, val1.lower(), val2.lower()).ratio()
            return similarity >= threshold

        # List comparison
        if isinstance(val1, list) and isinstance(val2, list):
            if len(val1) != len(val2):
                return False
            return all(self._values_match(v1, v2, threshold) for v1, v2 in zip(val1, val2))

        return False

    def _assess_conflict_severity(
        self,
        conflicts: List[Tuple[Any, Source]]
    ) -> str:
        """Assess severity of conflicts."""
        if len(conflicts) == 1:
            return "minor"
        elif len(conflicts) == 2:
            return "moderate"
        else:
            return "critical"

    def _generate_verification_notes(
        self,
        supporting_sources: List[Source],
        conflicts: List[Tuple[Any, Source]]
    ) -> Optional[str]:
        """Generate human-readable notes about verification."""
        notes = []

        if not supporting_sources:
            notes.append("No sources found supporting this claim.")

        if len(supporting_sources) == 1:
            notes.append("Verified by single source only - confidence limited.")

        if conflicts:
            notes.append(f"Found {len(conflicts)} conflicting value(s) in other sources.")

        primary_sources = [s for s in supporting_sources if s.source_type == SourceType.PRIMARY]
        if primary_sources:
            notes.append(f"Confirmed by {len(primary_sources)} primary source(s).")

        return " ".join(notes) if notes else None
