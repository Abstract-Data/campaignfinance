from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Annotated
from datetime import date, datetime


class TECRecordGetter(BaseModel):
    recordType: Optional[str]
    formTypeCd: Optional[str]
    schedFormTypeCd: Optional[str]
    reportInfoIdent: Optional[int]
    receivedDt: date
    infoOnlyFlag: Optional[bool]
    filerIdent: Optional[int]
    filerTypeCd: Optional[str]
    filerTitle: Optional[str]
    filerName: Optional[str]
    filerNameFormatted: Optional[str]
    filerFirstName: Optional[str]
    filerLastName: Optional[str]
    filerMiddleName: Optional[str]
    filerPrefix: Optional[str]
    filerSuffix: Optional[str]
    filerCompanyName: Optional[str]
    filerCompanyNameFormatted: Optional[str]
    expendInfoId: Optional[int]
    expendDt: Optional[date]
    expendAmount: Optional[float]
    expendDescr: Optional[str]
    expendCatCd: Optional[str]
    expendCatDescr: Optional[str]
    itemizeFlag: Optional[bool]
    travelFlag: Optional[bool]
    politicalExpendCd: Optional[bool]
    reimburseIntendedFlag: Optional[bool]
    srcCorpContribFlag: Optional[bool]
    capitalLivingexpFlag: Annotated[Optional[str], Field(max_length=1)]
    payeePersentTypeCd: Optional[str]
    payeeNameOrganization: Optional[str]
    payeeCompanyName: Optional[str]
    payeeCompanyNameFormatted: Optional[str]
    payeeNameLast: Optional[str]
    payeeNameSuffixCd: Optional[str]
    payeeNameFirst: Optional[str]
    payeeNamePrefixCd: Optional[str]
    payeeNameShort: Optional[str]
    payeeStreetAddr1: Optional[str]
    payeeStreetAddr2: Optional[str]
    payeeStreetCity: Optional[str]
    payeeStreetStateCd: Optional[str]
    payeeStreetCountyCd: Optional[str]
    payeeStreetCountryCd: Optional[str]
    payeeStreetPostalCode: Optional[str]
    payeeStreetPostalCode4: Optional[str]
    payeeStreetRegion: Optional[str]
    creditCardIssuer: Optional[str]
    repaymentDt: Optional[date]
    contributionInfoId: Optional[int]
    contributionDt: Optional[date]
    contributionAmount: Optional[float]
    contributionDescr: Optional[str]
    contributionCatCd: Optional[str]
    contributorNameOrganization: Optional[str]
    contributorNameLast: Optional[str]
    contributorNameSuffixCd: Optional[str]
    contributorNameFirst: Optional[str]
    contributorNamePrefixCd: Optional[str]
    contributorNameShort: Optional[str]
    contributorStreetCity: Optional[str]
    contributorStreetStateCd: Optional[str]
    contributorStreetCountyCd: Optional[str]
    contributorStreetCountryCd: Optional[str]
    contributorStreetPostalCode: Optional[str]
    contributorStreetPostalCode4: Optional[str]
    contributorStreetRegion: Optional[str]
    contributorEmployer: Optional[str]
    contributorOccupation: Optional[str]
    contributorJobTitle: Optional[str]
    contributorPacFein: Optional[str]
    contributorOosPacFlag: Optional[bool]
    contributorLawFirmName: Optional[str]
    contributorSpouseLawFirmName: Optional[str]
    contributorParent1LawFirmName: Optional[str]
    contributorParent2LawFirmName: Optional[str]
    # AbstractContributionHash: Optional[str]
    # AbstractExpenseHash: Optional[str]
    AbstractRecordUUID: UUID
    AbstractRecordUpdateDt: datetime = datetime.now()

    class Config:
        orm_mode = True
