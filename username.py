import random
from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel
from NameMutator import NameMutator  # Assuming you have the NameMutator class in a separate file

app = FastAPI()

class NameFormats(BaseModel):
    full_name: str
    f_last: List[str]
    f_dot_last: List[str]
    last_f: List[str]
    first_dot_last: List[str]
    first_l: List[str]
    first: List[str]

class NameFormatsWithEmail(NameFormats):
    f_last_email: List[str]
    f_dot_last_email: List[str]
    last_f_email: List[str]
    first_dot_last_email: List[str]
    first_l_email: List[str]
    first_email: List[str]

@app.get("/generate_names/", response_model=List[NameFormats])
async def generate_names(count: int = Query(10, description="Number of names to generate", ge=1, le=1000)):
    return generate_name_formats(count)

@app.get("/generate_names_with_email/", response_model=List[NameFormatsWithEmail])
async def generate_names_with_email(
    count: int = Query(10, description="Number of names to generate", ge=1, le=1000),
    domain: str = Query(..., description="Email domain to append")
):
    names = generate_name_formats(count)
    names_with_email = []

    for name in names:
        name_dict = name.dict()
        for key in name_dict:
            if key != 'full_name':
                name_dict[f"{key}_email"] = [f"{item}@{domain}" for item in name_dict[key]]
        names_with_email.append(NameFormatsWithEmail(**name_dict))

    return names_with_email

def generate_name_formats(count: int) -> List[NameFormats]:
    names = []
    
    with open("Fnames.txt") as f_names, open("Lnames.txt") as l_names:
        first_names = f_names.read().split()
        last_names = l_names.read().split()

    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        mutator = NameMutator(full_name)
        
        name_formats = NameFormats(
            full_name=full_name,
            f_last=list(mutator.f_last()),
            f_dot_last=list(mutator.f_dot_last()),
            last_f=list(mutator.last_f()),
            first_dot_last=list(mutator.first_dot_last()),
            first_l=list(mutator.first_l()),
            first=list(mutator.first())
        )
        
        names.append(name_formats)

    return names

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
