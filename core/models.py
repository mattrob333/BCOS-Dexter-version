"""
Data models for BCOS multi-source verification system.

These models support source attribution, confidence scoring,
and conflict detection across multiple data sources.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum


class SourceType(Enum):
    """Type of data source."""
    PRIMARY = "primary"  # Company website, official docs
    SECONDARY = "secondary"  # News articles, research reports
    TERTIARY = "tertiary"  # Third-party databases, aggregators
    VERIFICATION = "verification"  # Fact-checking services


class ConfidenceLevel(Enum):
    """Human-readable confidence levels."""
    VERY_HIGH = "very_high"  # 0.90-1.00
    HIGH = "high"  # 0.75-0.89
    MEDIUM = "medium"  # 0.50-0.74
    LOW = "low"  # 0.25-0.49
    VERY_LOW = "very_low"  # 0.00-0.24


@dataclass
class Source:
    """Represents a data source with full attribution."""
    url: str
    source_type: SourceType
    source_name: str  # e.g., "stripe.com", "TechCrunch", "Exa Research"
    date_accessed: datetime
    date_published: Optional[datetime] = None
    reliability_score: float = 1.0  # 0.0-1.0, how reliable is this source?

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'url': self.url,
            'source_type': self.source_type.value,
            'source_name': self.source_name,
            'date_accessed': self.date_accessed.isoformat(),
            'date_published': self.date_published.isoformat() if self.date_published else None,
            'reliability_score': self.reliability_score,
        }


@dataclass
class Conflict:
    """Represents a conflict between sources."""
    claim: str
    conflicting_values: List[Any]
    sources: List[Source]
    severity: str  # "minor", "moderate", "critical"
    resolution: Optional[str] = None  # How we resolved it (if we did)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'claim': self.claim,
            'conflicting_values': [str(v) for v in self.conflicting_values],
            'sources': [s.to_dict() for s in self.sources],
            'severity': self.severity,
            'resolution': self.resolution,
        }


@dataclass
class VerifiedFact:
    """
    A fact that has been verified across multiple sources.

    Core principle: Every fact must have source attribution.
    No hallucinations - if not found in sources, mark as unverified.
    """
    claim: str  # The fact being claimed
    value: Any  # The actual value (string, number, list, dict)
    verified: bool  # Was this verified across sources?
    confidence: float  # 0.0-1.0 confidence score
    sources: List[Source]  # All sources supporting this fact
    conflicts: List[Conflict] = field(default_factory=list)  # Any conflicts found
    notes: Optional[str] = None  # Additional context
    last_verified: datetime = field(default_factory=datetime.now)

    @property
    def confidence_level(self) -> ConfidenceLevel:
        """Get human-readable confidence level."""
        if self.confidence >= 0.90:
            return ConfidenceLevel.VERY_HIGH
        elif self.confidence >= 0.75:
            return ConfidenceLevel.HIGH
        elif self.confidence >= 0.50:
            return ConfidenceLevel.MEDIUM
        elif self.confidence >= 0.25:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

    @property
    def has_conflicts(self) -> bool:
        """Check if this fact has conflicts."""
        return len(self.conflicts) > 0

    @property
    def primary_sources(self) -> List[Source]:
        """Get primary sources only."""
        return [s for s in self.sources if s.source_type == SourceType.PRIMARY]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'claim': self.claim,
            'value': self.value,
            'verified': self.verified,
            'confidence': self.confidence,
            'confidence_level': self.confidence_level.value,
            'sources': [s.to_dict() for s in self.sources],
            'conflicts': [c.to_dict() for c in self.conflicts],
            'notes': self.notes,
            'last_verified': self.last_verified.isoformat(),
            'has_conflicts': self.has_conflicts,
        }


@dataclass
class VerifiedDataset:
    """
    A collection of verified facts about an entity (company, market, etc.)
    """
    entity_name: str  # e.g., company name
    entity_type: str  # "company", "market", "competitor"
    facts: List[VerifiedFact]
    overall_confidence: float  # Average confidence across all facts
    total_sources: int  # Total unique sources used
    verified_count: int  # Number of verified facts
    unverified_count: int  # Number of unverified claims
    conflict_count: int  # Number of facts with conflicts
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'entity_name': self.entity_name,
            'entity_type': self.entity_type,
            'facts': [f.to_dict() for f in self.facts],
            'overall_confidence': self.overall_confidence,
            'total_sources': self.total_sources,
            'verified_count': self.verified_count,
            'unverified_count': self.unverified_count,
            'conflict_count': self.conflict_count,
            'created_at': self.created_at.isoformat(),
        }

    @classmethod
    def from_facts(cls, entity_name: str, entity_type: str, facts: List[VerifiedFact]):
        """Create dataset from list of facts, calculating statistics."""
        verified = [f for f in facts if f.verified]
        unverified = [f for f in facts if not f.verified]
        with_conflicts = [f for f in facts if f.has_conflicts]

        # Calculate overall confidence (weighted by fact importance)
        if verified:
            overall_conf = sum(f.confidence for f in verified) / len(verified)
        else:
            overall_conf = 0.0

        # Count unique sources
        all_sources = set()
        for fact in facts:
            for source in fact.sources:
                all_sources.add((source.url, source.source_name))

        return cls(
            entity_name=entity_name,
            entity_type=entity_type,
            facts=facts,
            overall_confidence=overall_conf,
            total_sources=len(all_sources),
            verified_count=len(verified),
            unverified_count=len(unverified),
            conflict_count=len(with_conflicts),
        )
