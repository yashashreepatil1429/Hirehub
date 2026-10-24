from __future__ import annotations

from typing import Any, Dict, List

from app.services.matching_service import MatchingService


class RecommendationService:
    def __init__(self, matching_service: MatchingService | None = None):
        self.matching_service = matching_service or MatchingService()

    def recommend_jobs(self, candidate: Dict[str, Any], jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ranked = []
        for job in jobs:
            match = self.matching_service.calculate(job, candidate)
            ranked.append({**job, 'match_percent': match['match_percent'], 'matched_skills': match['matched_skills'], 'missing_skills': match['missing_skills']})
        return sorted(ranked, key=lambda item: item['match_percent'], reverse=True)
