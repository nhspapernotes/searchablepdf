from collections import defaultdict
import re

from flags import flag_list
from exporters import exports

"""
Each flag takes the format of (matcher, scores) where the matcher
is either a regex or a function and the scores are a dictionary.

Matcher regex: If the expression matches then the flag is raised and the
score used but if the expression does not match then the score is ignored

Matcher function: Return true to use the score, false to ignore the score.

Score dictionary: Each key refers to the vote towards a given
classification/export method. Each score is a two part tuple of
adder and multiplier. Adders are added together and multipliers are
multiplied together as the score is built up, then the adder and multiplier
are multiplied for a final score.

For example:
  (1, 0) => 1 point to add but will zero the final score
  (0, 1) => No effect on adder and no effect on final score
  (0, 0.25) => No effect on adder and final score is 25%

"""

"""
test_flag(Flag, String) => {String: (Float, Float)}
"""
def test_flag(flag, text_contents, image):
  (matcher, scores) = flag
  
  if hasattr(matcher, "__call__"):
    matched = matcher(text_contents, image)
  
  else:
    result = re.search(matcher, text_contents)
    matched = (result != None)
  
  # If the flag matches something then return the scores to be added
  if matched:
    return scores
  else:
    return {"others": (0, 1)}


"""
scan_letter(String) => [(String, Float)]
"""
def scan_letter(text_contents, image):
  text_contents = text_contents.lower()
  
  export_scores = defaultdict(lambda: list([0, 1]))
  
  for flag in flag_list:
    (matcher, scores) = flag
    
    flag_scores = test_flag(flag, text_contents, image)
    
    for e in exports.keys():
      if e in flag_scores:
        (adder, multiplier) = flag_scores[e]
      else:
        (adder, multiplier) = flag_scores["others"]
      
      [epoints, emultiplier] = export_scores[e]
      export_scores[e] = [epoints + adder, emultiplier * multiplier]
  
  return rank_scores(export_scores)

"""
rank_scores({String: (Float, Float)}) => [(String, Float)]
"""
def rank_scores(combined_scores):
  score_dictionary = {l:s[0] * s[1] for l, s in combined_scores.items()}
  sorted_scores = sorted(score_dictionary.items(), key=lambda x: x[1])
  return sorted_scores[::-1]

"""
score_letter((Float, Float)) => Float 
"""
def score_letter(combo_points):
  [points, multiplier] = combo_points
  
  return points * multiplier

"""

"""
def categorise_letter(text_contents, image, debug=False):
  scores = scan_letter(text_contents, image)
  
  export_function = exports[scores[0][0]]
  json_export = export_function(text_contents)
  
  if debug:
    for name, score in scores:
      print(name + ": " + str(score))  
    
    print("")
    print(json_export)
    print("\n")
    
  else:
    return json_export



if __name__ == '__main__':
  text_contents = """
Clinic Date
NHS
This Hospital
Somewhere
NW4 FTP
Joe Johnson, 1983-11-10, NHS number:4680200921
Dear patient,
Diagnoses:
Asthma
Medications:
Enoxaparin
Gentamycin
Clindamycin
Codeine
Asprin
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ultrices neque mattis vestibulum
imperdiet. Nulla sit amet tincidunt quam. Pellentesque malesuada tristique sollicitudin. Pellentesque
eu augue finibus, posuere sem auctor, ultricies nibh. Curabitur molestie lectus pellentesque,
malesuada augue nec, maximus lorem. Maecenas viverra velit mauris, id rhoncus libero porta sit
amet. Curabitur molestie gravida bibendum. Nunc posuere magna pellentesque felis aliquam, sit
amet vestibulum magna pulvinar, Ut vulputate vulputate urna, ac porttitor ex vehicula elementum
Duis ut vulputate elit. Nullam sodales dui vestibulum porta eleifend. Mauris a elementum nunc, quis
volutpat urna, Vivamus auctor ex id eleifend pellentesque. Donec congue leo lacus, sed iaculis velit
fringilla vel. Ut vehicula turpis vel tincidunt vulputate. Nullam aliquam enim sit amet fringilla tincidunt.
Cras eu mi massa, in pulvinar tempor nulla in cursus, Aenean a elit eget enim bibendum
pellentesque. Nulla at felis sagittis, consequat orci sed, cursus sapien.


"""
  categorise_letter(text_contents, None, debug=True)
