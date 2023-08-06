import os
from typing import Optional

from fastapi import APIRouter, Depends, Request, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session

from erre2.authentication import get_current_user, check_admin
from erre2.database import schemas, models
from erre2.database.crud import get_summaries, get_summary, create_summary, update_summary, get_summaries_course, \
    remove_summary, get_server
from erre2.dependencies import get_db, save_file
from erre2.integrations import telegram_send_message

router = APIRouter(
    prefix="/summary",
    tags=["summaries"],
    responses={404: {"description": "Not found"}, 204: {"description": "Removed"}}
)


@router.get("/", tags=["summaries"], response_model=schemas.SummaryList)
async def read_summary_list(request: Request, course_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Returns list of all summaries, or just one.
    """
    if not course_id:
        summaries = get_summaries(db)
        return schemas.SummaryList(summaries=summaries)
    summaries = get_summaries_course(db, course_id)
    return schemas.SummaryList(summaries=summaries)


@router.patch("/{summary_id}", tags=["summaries"], response_model=schemas.Summary)
async def patch_summary(summary_id: int, update: str = Form(...), file: UploadFile = File(...),
                        db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Allows summary patching
    {"summary":{"sid":0,"author_id":2,"course_id":1,"name":"Pippo",
    "filename":"string","downloads":0},"description":"Ciao"}
    """
    s = get_summary(db, summary_id)
    if not s:
        raise HTTPException(404, "Not found.")
    old_filename = s.filename
    update: schemas.SummaryUpdate = schemas.SummaryUpdate.parse_raw(update)
    filename = await save_file(file, update.summary)
    s: schemas.Summary = update_summary(db, update.summary, summary_id, update.description, file)
    server: models.Server = get_server(db)
    if old_filename != s.filename:
        os.remove(os.path.join("Files", old_filename))
    telegram_send_message("""🌐 <b>Aggiornamento su {}</b>
{} è stato aggiornato:

{}

⬇️ <a href=\"{}\">Scarica</a>"""
                          .format(server.name, s.name, update.description,
                                  "https://navigator.erre2.fermitech.info/erre2/{}/download/{}"
                                  .format(os.getenv("ROOT_URL"), s.sid)))
    return s


@router.put("/{summary_id}")
async def put_summary(summary_id: int, update: schemas.SummaryName, db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):
    """
    Allows summary name to be updated
    """
    s: models.Summary = get_summary(db, summary_id)
    if not s:
        raise HTTPException(404, "Not found.")
    s.name = update.name
    db.commit()
    db.refresh(s)
    return s


@router.delete("/{summary_id}")
async def delete_summary(summary_id: int, db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    """
    Allows the removal of a summary
    """
    s: models.Summary = get_summary(db, summary_id)
    if not s:
        raise HTTPException(404, "Not found.")
    if s.author_id != current_user.uid and not check_admin(current_user):
        raise HTTPException(403, "Only the owner can delete the summary.")
    os.remove(os.path.join("Files", s.filename))
    remove_summary(db, summary_id)
    return HTTPException(204, "Removed with success")


@router.post("/", tags=["summaries"], response_model=schemas.Summary)
async def create_summary_(summary: str = Form(...), file: UploadFile = File(...),
                          current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Allows the creation of a new summary
    {"sid": 0,"author_id": 2,"course_id": 1,"name": "Pippo","filename": "string","downloads": 0}
    """
    summary = schemas.Summary.parse_raw(summary)
    s: schemas.Summary = create_summary(db, summary, file)
    await save_file(file, s)
    server: models.Server = get_server(db)
    msg = """🌐 <b>Nuovo upload su {}</b>
{} è stato aggiunto sulla piattaforma.
            
⬇️ <a href=\"{}\">Scarica</a>""".format(
        server.name, s.name,
        "https://navigator.erre2.fermitech.info/erre2/{}/download/{}".format(os.getenv("ROOT_URL"), s.sid))
    telegram_send_message(msg)
    return s


@router.get("/download/{summary_id}", tags=["summaries"], response_model=schemas.Summary)
async def download_summary(summary_id: int, db: Session = Depends(get_db)):
    """
    Allows the download of a summary
    """
    s = get_summary(db, summary_id)
    if not s:
        raise HTTPException(status_code=404, detail="Couldn't find summary")
    s.downloads += 1
    db.commit()
    return s
