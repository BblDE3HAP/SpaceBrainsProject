﻿using BusinessLogic.DTO.Account;
using Domain.Entities.Users;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLogic.Services.Base
{
    public interface IAuthenticationService
    {
        bool CheckUser(string login, string password);
        bool IsAdmin(string login);
        bool IsSuperAdmin(string login);
        bool CheckLogin(string loginToCheck);
        void AdminRegistration(UserDTO userRegistrationData);
        void UserRegistration(UserDTO userRegistrationData, int adminId);
        User GetUserByLogin(string login);
        int GetAdminIdByLogin(string adminLogin);
        void ChangePassword(string login, string newPassword);
    }
}
