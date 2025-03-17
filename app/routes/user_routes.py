from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud import user_crud
from app.auth.auth_handler import create_token, decode_token
from app.auth.auth_bearer import JWTBearer
from app.models.user import User as UserModel
from app.oso_rbac.oso_policy import oso
from app.models.resource import AppResource  
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if user_crud.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    created = user_crud.create_user(user.username, user.email, user.password)
    return UserOut(**created)

@router.post("/login")
def login(user: UserLogin):
    auth_user = user_crud.authenticate_user(user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": auth_user["username"], "role": auth_user["role"]})
    return {"access_token": token}

@router.get("/me", response_model=UserOut, dependencies=[Depends(JWTBearer())])
def read_profile(token: str = Depends(JWTBearer())):
    payload = decode_token(token)
    user = user_crud.get_user_by_username(payload["sub"])
    user_obj = UserModel(username=user['username'], role=user['role'])
    user_obj.username = user['username']
    user_obj.role = user['role']
    
    # Create a Resource object instead of using a string
    profile_resource = AppResource("profile")
    print(profile_resource,'profile resource')
    # RBAC Check using Oso with the Resource object
    if not oso.is_allowed(user_obj, "read", profile_resource):
        raise HTTPException(status_code=403, detail="Access denied by RBAC")
    return UserOut(**user)

@router.get("/admin/secret", dependencies=[Depends(JWTBearer())])
def admin_only_route(token: str = Depends(JWTBearer())):
    payload = decode_token(token)
    user = user_crud.get_user_by_username(payload["sub"])
    user_obj = UserModel(username=user['username'], role=user['role'])
    user_obj.username = user['username']
    user_obj.role = user['role']
    
    # Create a Resource object instead of using a string
    profile_resource = AppResource("profile")
    
    if not oso.is_allowed(user_obj, "manage", profile_resource):
        raise HTTPException(status_code=403, detail="Admins only 🚫 can view their profile")
    
    return {"message": "Welcome Admin 👑"}

@router.patch("/role/update")
def update_user_role(username: str, new_role: str, token: str = Depends(JWTBearer())):
    payload = decode_token(token)
    current_user = user_crud.get_user_by_username(payload["sub"])
    
    # Only allow admin to update roles
    user_obj = UserModel(username=current_user["username"], role=current_user["role"])
    if not oso.is_allowed(user_obj, "manage", "profile"):
        raise HTTPException(status_code=403, detail="Admins only can update the role")
    
    updated = user_crud.update_user_role(username, new_role)
    return {"message": f"Role updated for {username} to {new_role}"}


@router.delete("/delete")
def delete_user(username: str, token: str = Depends(JWTBearer())):
    # Get current user
    payload = decode_token(token)
    current_user = user_crud.get_user_by_username(payload["sub"])
    
    # RBAC Enforcement - Use AppResource consistently
    user_obj = UserModel(username=current_user["username"], role=current_user["role"])
    if not oso.is_allowed(user_obj, "manage", AppResource("profile")):
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    # Proceed with deletion
    result = user_crud.delete_user_by_username(username)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    return {"message": f"User '{username}' has been deleted"}

