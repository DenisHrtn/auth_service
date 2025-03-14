from fastapi import APIRouter, Depends, Query, Request, Response

from app.application.interactors.profiles.get_all_profiles_interactor import (
    GetAllProfilesInteractor,
)
from app.application.interactors.profiles.update_profiles_interactor import (
    UpdateProfilesInteractor,
)
from app.application.use_cases.profiles.dto import UpdateProfileDTO
from app.containers import container
from app.infra.schemas.profile_schemas import UpdateProfileSchema
from app.infra.utils.auth_required import auth_required

router = APIRouter(tags=["profiles"])


@router.patch("/update-profile/{profile_id}")
@auth_required
async def update_profile(
    request: Request,
    profile_id: int,
    schema: UpdateProfileSchema,
    update_profile_interactor: UpdateProfilesInteractor = Depends(
        lambda: container.update_profile_interactor()
    ),
):
    token = request.headers.get("Authorization")
    extracted_token = token.split(" ")[1]

    update_profile_dto = UpdateProfileDTO(
        schema.first_name, schema.last_name, schema.info, schema.speciality
    )

    result = await update_profile_interactor.execute(
        extracted_token, profile_id, update_profile_dto
    )

    return Response(f"Profile updated: {result}", status_code=200)


@router.get("/get-all-profiles")
@auth_required
async def get_all_profiles(
    request: Request,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    get_profiles_interactor: GetAllProfilesInteractor = Depends(
        lambda: container.get_all_profiles_interactor()
    ),
):
    result = await get_profiles_interactor.get_all_profiles_with_users(offset, limit)

    return result
