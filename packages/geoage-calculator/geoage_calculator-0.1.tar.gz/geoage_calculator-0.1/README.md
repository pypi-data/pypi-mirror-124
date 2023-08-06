# GeoAge Calculator
GeoAge Calculator is a really simple but useful package for working with datasets that include reported geological ages in inconsistent formats. It provides two main functions: `geo_age_lookup` and `age_range_lookup`.

## Installation
At the moment this package is only available via git. You can either download the latest version and isntall into your working directory or install via pip using:

    pip install git+https://github.com/SSJenny90/geoage-calculator.git#egg=geoage-calculator

## How to use
For a reported geological age in name format, e.g. 'Cryogenian', `age_range_lookup` will convert this to a tuple consisting of upper and lower age bounds. Over 750 official and unofficial geological names are currently supported.

    >>>from geoage_calculator import age_range_lookup, geo_age_lookup
    >>>age_range_lookup('Cryogenian')
    (37.2, 40.4)


For numerical age data reported in millions of years (Ma), `geo_age_lookup` will return an `OrderedDict` of official age names based on the Internation Commission on Stratigraphy. Values are returned as geochronological names rather than stratigraphic names. 

    >>>geo_age_lookup(143.6)
    OrderedDict([('eon', 'phanerozoic'),
             ('era', 'mesozoic'),
             ('period', 'cretaceous'),
             ('epoch', 'early-cretaceous'),
             ('age', 'berriasian')])


## Using with Pandas
If you have a pandas dataframe of age values and want to use these function to expand results out into additional columns, you can do so like this:

    >>>df = pd.DataFrame(['cambrian','jurassic','oligocene','baigendzinian'], columns=['age_data'])
    >>>print(df)
           age_data
    0      cambrian
    1      jurassic
    2     oligocene
    
    >>>df['age_lower'], df['age_upper'] = zip(*df['age_data'].map(age_range_lookup))
    >>>print(df)
            age_data  age_lower  age_upper
    0       cambrian     485.40      541.0
    1       jurassic     145.00      201.3
    2      oligocene      23.03       33.9
    3  baigendzinian     275.60      284.4

OR

    >>>df = pd.DataFrame([56,174,366,527], columns=['age_data'])
    >>>print(df)
       age_data
    0        56
    1       174
    2       366
    3       527
    
    >>>tmp = df.apply(lambda row: geo_age_lookup(row['age_data']), axis=1, result_type='expand')
    >>>df = pd.concat([df, tmp], axis=1)
    >>>print(df)
       age_data          eon        era     period            epoch        age
    0        56  phanerozoic   cenozoic  paleogene        paleocene  thanetian
    1       174  phanerozoic   mesozoic   jurassic  middle-jurassic   aalenian
    2       366  phanerozoic  paleozoic   devonian    late-devonian  famennian
    3       527  phanerozoic  paleozoic   cambrian     terreneuvian    stage 2

