functionalGroups = [
    ["Carboxylic acid", "oic acid", 3],
    ["Aldehyde", "al", 3],
    ["Amine", "amine", 2],
    ["Alcohol", "ol", 1],
    ["Ketone", "one", 2],
    ["Ester", "oate"],
    ["none", "e"]
]

prefixes = [
    ["di", 2],
    ["tri", 3],
    ["tetra", 4],
    ["penta", 5],
    ["hexa", 6]
]

parentNumbers = [
    ["meth", 1],
    ["eth", 2],
    ["prop", 3],
    ["but", 4],
    ["pent", 5],
    ["hex", 6],
    ["hept", 7],
    ["oct", 8],
    ["non", 9],
    ["dec", 10]
]

SUBSTITUENT_DNE = -1
SUBSTITUENT_CHAIN = 0
SUBSTITUENT_MODIFIED_CHAIN = 1
SUBSTITUENT_HALOGEN = 2
substituents = [
    [SUBSTITUENT_MODIFIED_CHAIN, "isopropyl", 3],
    [SUBSTITUENT_MODIFIED_CHAIN, "tert-butyl", 4],
    [SUBSTITUENT_CHAIN, "methyl", 1],
    [SUBSTITUENT_CHAIN, "ethyl", 2],
    [SUBSTITUENT_CHAIN, "propyl", 3],
    [SUBSTITUENT_CHAIN, "butyl", 4],
    [SUBSTITUENT_CHAIN, "pentyl", 5],
    [SUBSTITUENT_CHAIN, "hexyl", 6],
    [SUBSTITUENT_CHAIN, "heptyl", 7],
    [SUBSTITUENT_CHAIN, "octyl", 8],
    [SUBSTITUENT_CHAIN, "nonyl", 9],
    [SUBSTITUENT_CHAIN, "decyl", 10],
    [SUBSTITUENT_HALOGEN, "fluoro", "F"],
    [SUBSTITUENT_HALOGEN, "chloro", "Cl"],
    [SUBSTITUENT_HALOGEN, "bromo", "Br"],
    [SUBSTITUENT_HALOGEN, "iodo", "I"],
    [SUBSTITUENT_DNE,"",0]
]