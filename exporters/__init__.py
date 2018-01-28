from . import discharge_summary
from . import ecg
from . import clinic_letter

exports = {
  "discharge summary": discharge_summary.main,
  "ecg": ecg.main,
  "clinic letter": clinic_letter.main,
}