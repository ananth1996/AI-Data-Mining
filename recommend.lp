% CS-E4800 Artificial intelligence
% Round: Data Mining
%
% Base Encoding for the ASP Exercise: Optimizing Itemsets for Recommendations
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing details
% on the basis of descriptions given as well as general understanding of
% the problem. In some cases, you might need serveral (similar) rules,
% or could introduce an auxiliary predicate to help with the definition.

% Association rules are described in terms of three predicates:
%
% - head(R,I): item I is the (unique) head item of R
% - body(R,I): item I belongs to the body of R
% - confidence(R,L): the confidence of rule R is C
%
% In the above, rules and items have just integer ids.
%
% The human-readable names of the items are given by:
%
% - name(I,"name"): where "name" is the name of item I
%
% The intended way of running the program is:
%
% $ gringo recommend.lp names.lp scores.lp instances/rules.lp \
%   | clasp --quiet=1 --project --opt-mode=optN
%
% which will find out all optimal solutions for you.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TODO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Extract the domains of interest: predicates rule/1 and item/1

rule(R) :- ???.
item(I) :- ???.

% Parameters for the problem (bag dimensions): leave as is

#const minsize = 3.
#const maxsize = 6.

% Choose items to the bag using in/1 predicate
% so that the limits above are respected

??? { in(I) ??? } ???.

% Detect active association rules
% (whose body items are in the bag but not the head item)
active(R) :- rule(R); in(I): body(R,I); not in(I): head(R,I).

% At least three distinct recommendations must result from active rules
:- #count { ??? : active(R), rule(R), ??? } ???.

% Detect which active rule has a highest confidence level
% (break ties using the rule id). Beware that you can compare
% pairs (S,R) using operators like < and <=.
%
% Confidence levels are given in scores.lp

best(R) :- active(R), score(R,S), ??? .

% Maximize the confidence level of the best rule
#maximize { ???@??? : best(R), ??? }.

% Identify the items in the bag by their names (see names.lp)
bag(N) :- ???.

% Identify the recommended items by their names (see names.lp)
recommend(N) :- active(R), ???.

#show bag/1.
#show recommend/1.
