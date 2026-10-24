from __future__ import annotations

from typing import Any, Dict, List


class MatchingService:
    @staticmethod
    def calculate(job: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
        candidate_skills = {skill.strip().lower() for skill in candidate.get('skills', [])}
        job_skills = {skill.strip().lower() for skill in job.get('skills', [])}
        matched = sorted(candidate_skills & job_skills)
        missing = sorted(job_skills - candidate_skills)
        skill_score = (len(matched) / max(len(job_skills), 1)) * 60
        exp_score = 20 if candidate.get('experience', 0) >= (job.get('experience_min', 0) or 0) else 0
        loc_score = 10 if str(candidate.get('location', '')).lower() == str(job.get('location', '')).lower() else 0
        salary_score = 10 if candidate.get('expected_salary', 0) >= job.get('salary_min', 0) else 0
        total = int(round(skill_score + exp_score + loc_score + salary_score))
        return {
            'match_percent': min(100, max(0, total)),
            'matched_skills': matched,
            'missing_skills': missing,
            'job_id': job.get('id'),
        }

    @staticmethod
    def match_jobs(candidate: Dict[str, Any], jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []
        for job in jobs:
            result.append(MatchingService.calculate(job, candidate))
        return sorted(result, key=lambda item: item['match_percent'], reverse=True)
