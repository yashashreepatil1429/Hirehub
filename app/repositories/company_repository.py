from __future__ import annotations

from typing import Any, Dict, List

from app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository):
    collection_name = 'companies'

    def create(self, company: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(company)

    def list_companies(self) -> List[Dict[str, Any]]:
        return self.find_all()

    def get_by_name(self, name: str) -> Dict[str, Any] | None:
        return self.find_one({'name': name})

    def get_by_id(self, company_id: str) -> Dict[str, Any] | None:
        return self.find_by_id(company_id)
