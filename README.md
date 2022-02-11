## University of Utah Catalog Course Parser

University of Utah catalog parser for course information per semester.

Was mainly created for a free API that could be used against course lists, for any reason.

Works for catalog HTML layout as of Feb. 10, 2022.

## Usage

JSON static file serving is available through Github Pages for this repo.

Access semester subjects:

```
http://ethanpippin.com/UofUCatalogParser/{ MainCampus | AsiaCampus | UOnline }/{ Semester }/subjects.json
```

Access semester subject catalog:
```
http://ethanpippin.com/UofUCatalogParser/{ MainCampus | AsiaCampus | UOnline }/{ Semester }/{ Subject Abbreviation}.json
```

Note that for subjects that have multiple components, like `OC TH`, spaces have been replaced with dashes `-`: `OC-TH`

Examples:

- http://ethanpippin.com/UofUCatalogParser/MainCampus/Spring2022/subjects.json
- http://ethanpippin.com/UofUCatalogParser/MainCampus/Spring2022/CS.json


## Parser

Install requirements, run `parser.py`.

## Next Steps

- [ ] TODO comments completed
- [ ] Create JSON files for base which will say what campuses are available with their semester keys
- [ ] Look at parsing course pages for pre-reqs and description
