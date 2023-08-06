# epics-linter

A project to lint and provide useful commentary on EPICS database files

**Currently this project is in a very early state, as time passes, more support filetypes/field will be added.**

## Installation
`pip3 install .`

## Utilization

`python3 -m epics_linter file.db`

## Examples

```
record(ai, "test", oops) {
    field(DESC, "$(DESCRIPTION)")
    field(DTYP, "stream")
    field(EGU, "$(EGU)")
    [...]
}
```

```sh 
python3 -m epics_linter file.db 
>> Too many arguments at 1:20
```

```
record(ai, "test") {
    field(DESC, "a way too long description name that does not fit in the maximum limit")
    field(DTYP, "stream")
    field(EGU, "$(EGU)")
    [...]
}
```

```sh 
python3 -m epics_linter file.db 
>> Record description too long (maximum of 40) at 2:17 to 2:89
```
