## University of Utah Catalog Course Parser

University of Utah catalog parser for course information per semester.

Was mainly created for a free API that could be used against course lists, for any reason.

Works for catalog HTML layout as of Feb. 10, 2022.

## Usage

Access semester subjects::

```
http://ethanpippin.com/UofUCatalogParser/{ MainCampus | AsiaCampus | UOnline }/{ Semester }/subjects.json
```

Access semester subject catalog:
```
http://ethanpippin.com/UofUCatalogParser/{ MainCampus | AsiaCampus | UOnline }/{ Semester }/{ Subject Abbreviation}.json
```

Note that for subjects that have multiple components, like `OC-TH`, spaces have been replaced with dashes `-`

Examples:

```
http://ethanpippin.com/UofUCatalogParser/MainCampus/Spring2022/subjects.json
http://ethanpippin.com/UofUCatalogParser/MainCampus/Spring2022/CS.json
```

## Parser

Install requirements, run `parser.py`.

## Next Steps

- [ ] Fill in remaining semesters
- [ ] Create `available.json` files for base which will say what campuses are available with their semester keys
