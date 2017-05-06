# Proportional Representation in the US House

This is a simple example of what a proportional system would look like in the US House. Each state has its delegation doubled, and one-half of the delegation is to be appointed proportioanlly. The Presidential vote-share is used as the party-line share, in the absense of better data (not every state has senate elections every cycle, and unconstested or unbalanced house races make the house popular vote a flawed metric.)

Note that, in both the original and proportional systems, smaller states tend to be less proportional. This is a natural consequence of a smaller delegation, and a correction factor will be introduced in the future.

## How to run:

`./proprep.py <year> [--latex]`

Where `<year>` is the year you want to generate maps for (only 2012 and 2016 are currently available), and `[--latex]` enables generation of a LaTeX table of results.

##Example

This is an example of the program on the 2012 election. First, the existing misrepresentation map:

![2012-old-map](out/2012_old_map.svg)

And then the proportional map:

![2012-prop-map](out/2012_prop_map.svg)
