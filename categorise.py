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
def test_flag(flag, text_contents):
  (matcher, scores) = flag
  
  if hasattr(matcher, "__call__"):
    matched = matcher(text_contents)
  
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
def scan_letter(text_contents):
  text_contents = text_contents.lower()
  
  export_scores = defaultdict(lambda: list([0, 1]))
  
  for flag in flag_list:
    (matcher, scores) = flag
    
    flag_scores = test_flag(flag, text_contents)
    
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
  return sorted(score_dictionary.items(), key=lambda x: x[1])

"""
score_letter((Float, Float)) => Float 
"""
def score_letter(combo_points):
  [points, multiplier] = combo_points
  
  return points * multiplier


if __name__ == '__main__':
  text_contents = """
NHS
Blood and Transplant
Charcot Road
Colindale
London
NW9 5GB
11 November 2014
Private and Confidential
www.blood.co.uk
Dear Mx
Thank you very much for getting in touch with us.
Your query has been passed on to our department for further comment. I can see
that Vivian did explain that our IT system is currently unable to offer the options of
non-specific gender title of Mx.
It is not a problem if a transgender person wishes to donate providing we establish
the donor's preferred gender i.e., male or female. Once we have established the
preferred gender of the donor, we will treat the donor according to his/her preference.
Trans men FtM donors will be treated as male donors regardless of their female
characteristics and similarly, we will treat trans women MtF donors as female donors
regardless of their male characteristics. Again, the donor has to decide whether they
will be gendered as male or female before we can proceed. It is clinically important
for us to identify whether the donor is male or female in order to ensure we only
accept donations when it is safe for both donors and recipients. Our haemoglobirn
testing on session have different acceptance levels between male and female
donors. We have a much higher cut-off level for male donors than female donors. I
must apologise for the wrong information you have been given. Male donors tend to
have a higher haemoglobin count compared to female donors but not necessarily the
platelet count. There are various factors why this is the case and one of these are the
high levels of testosterone among the male population including those on
testosterone therapy i.e. trans men donors.
Hoping you will find the information useful. Please feel free to contact our helpline on
0300 123 23 23 if you need to discuss further and request to be put through to the
Clinical Support Team. We are available between 8am - 8pm Monday to Friday,
9:30am to 5:00pm on weekends.
With best wishes and kindest regards.
Yours sincerely
Alvin Fabiana
Senior Nurse Practitioner
Business ABOU
Forum
Save a life
Give blood
Disability0C
Bullding
disablity-smar
organisation
SABL
"""
  scores = scan_letter(text_contents)
  
  for name, score in scores[::-1]:
    print(name + ": " + str(score))
