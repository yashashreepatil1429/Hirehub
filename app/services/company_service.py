from __future__ import annotations

from typing import Any, Dict, List

from app.repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, company_repository: CompanyRepository | None = None):
        self.company_repository = company_repository or CompanyRepository()

    def list_companies(self) -> List[Dict[str, Any]]:
        return self.company_repository.list_companies()

    def get_by_id(self, company_id: str) -> Dict[str, Any] | None:
        return self.company_repository.get_by_id(company_id)
