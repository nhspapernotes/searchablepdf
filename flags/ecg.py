from opencv import ecg

flags = [
  (lambda text, image: ecg.is_ecg(image), {
    "ecg": (1, 1),
    "others": (0, 0.25),
  }),
]
