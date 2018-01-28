flags = [
  (r"date of discharge", {
    "discharge summary": (1, 1),
    "others": (0, 0.25),
  }),
  
  (r"discharge summary", {
    "discharge summary": (1, 1),
    "others": (0, 0),
  }),
  
  (r"ecg", {
    "ecg": (1, 1),
    "others": (0, 1),
  }),
  
  ((lambda x: True), {
    "discharge summary": (0, 0),
    "others": (1, 1),
  })
]
