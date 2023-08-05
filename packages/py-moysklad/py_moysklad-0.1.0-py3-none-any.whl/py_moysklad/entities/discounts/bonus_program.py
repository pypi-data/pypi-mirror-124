from py_moysklad.entities.discounts.discount import Discount


class BonusProgram(Discount):
    earnRateRoublesToPoint: int
    spendRatePointsToRouble: int
    maxPaidRatePercents: int
    postponedBonusesDelayDays: int
