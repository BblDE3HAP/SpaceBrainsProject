﻿using BusinessLogic.Services.Base;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using WebAI.Models.Account;
using System.Web.Security;
using System.Threading;
using AutoMapper;
using BusinessLogic.DTO.Account;
using Utility.Helpers;
using Utility.enums;

namespace WebAI.Controllers
{
    [Authorize]
    public class AccountController : Controller
    {
        
        IAuthenticationService _authenticationService;
        IMapper _mapper;

        public AccountController(IAuthenticationService authenticationService, IMapper mapper)
        {
            _authenticationService = authenticationService;
            _mapper = mapper;
        }

        //public ActionResult AccountManage()
        //{

        //}
        
        public ActionResult AddUser()
        {
            if (IsCurrentUserSuperAdmin())
                return RedirectToAction("AdminRegistration");
            else
                return RedirectToAction("UserRegistration");
        }
        [HttpGet]
        public ActionResult AdminRegistration()
        {
            ViewBag.ActionName = "AdminRegistration";
            ViewBag.FormName = "Администратора";
            return View("UserRegistration");
        }

        
        [HttpPost]
        public ActionResult AdminRegistration(UserRegistrationViewModel userRegistrationViewModel)
        {
            if (ModelState.IsValid)
            {
                _authenticationService.AdminRegistration(_mapper.Map<UserRegistrationViewModel, UserDTO>(userRegistrationViewModel));
                
                return RedirectToAction("UsersList", "User", new { id = (int)RolesEnum.Root });
            }
            else
                return View("UserRegistration", userRegistrationViewModel);
            
            
        }

        
        [HttpGet]
        public ActionResult UserRegistration()
        {
            ViewBag.ActionName = "UserRegistration";
            ViewBag.FormName = "Пользователя";
            return View("UserRegistration");
        }

        
        [HttpPost]
        public ActionResult UserRegistration(UserRegistrationViewModel userRegistrationViewModel)
        {
            var adminId = GetCurrentAdminId();
            if (ModelState.IsValid)
            {
                _authenticationService.UserRegistration(_mapper.Map<UserRegistrationViewModel, UserDTO>(userRegistrationViewModel), adminId);
                
                return RedirectToAction("UsersList", "User", new { id = (int)RolesEnum.Admin });
            }
            else
                return View("UserRegistration", userRegistrationViewModel);
        }

        [AllowAnonymous]
        [HttpGet]
        public ActionResult LogIn()
        {
            ViewBag.IsLoginForm = true;
            return View();
        }

        [AllowAnonymous]
        [HttpPost]
        public ActionResult LogIn(LogInViewModel logInModel)
        {
            if (!ModelState.IsValid)
                return View(logInModel);
            if (_authenticationService.CheckUser(logInModel.Login, logInModel.Password))
            {
                
                string login = logInModel.Login;
                FormsAuthentication.SetAuthCookie(login, true);
                AdminIdRemember.Id = GetCurrentAdminId(login);
                BusinessLogic.DTO.PersonIdRemember.Id = 0;
                return RedirectToAction("Index", "Home", _authenticationService.IsSuperAdmin(login));
            }
            return RedirectToAction("LogIn",logInModel);
        }

        [HttpGet]
        public ActionResult ChangePassword()
        {
            return View();
        }
        [HttpPost]
        public ActionResult ChangePassword(ChangePasswordViewModel changePasswordModel)
        {
            
            if (ModelState.IsValid)
            {
                _authenticationService.ChangePassword(GetCurrentUserName(), changePasswordModel.NewPassword);

                return RedirectToAction("Index", "Home", _authenticationService.IsSuperAdmin(GetCurrentUserName()));
            }
            else
                return View(changePasswordModel);
        }

        public ActionResult LogOut()
        {
            FormsAuthentication.SignOut();
            AdminIdRemember.Id = 0;
            return Redirect(FormsAuthentication.LoginUrl);
        }

        [HttpGet]
        public ActionResult CurrentUser()
        {
            
            return PartialView("_CurrentUser", GetCurrentUserName());
        }

        [HttpGet]
        public JsonResult CheckLogin(string login)
        {
            var result = _authenticationService.CheckLogin(login);
            return Json(result, JsonRequestBehavior.AllowGet);
        }

        [HttpGet]
        public JsonResult CheckPassword(string oldPassword)
        {
            var result = _authenticationService.CheckUser(GetCurrentUserName(), oldPassword);
            return Json(result, JsonRequestBehavior.AllowGet);
        }
        

        string GetCurrentUserName()
        {
            return Thread.CurrentPrincipal.Identity?.Name;
            
        }

        int GetCurrentAdminId()
        {
            return _authenticationService.GetAdminIdByLogin(GetCurrentUserName());
        }

        int GetCurrentAdminId(string login)
        {
            return _authenticationService.GetAdminIdByLogin(login);
        }

        bool IsCurrentUserSuperAdmin()
        {
            return _authenticationService.IsSuperAdmin(GetCurrentUserName());
        }

    }
}