﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace WebAI.Models.Account
{
    public class EditUserViewModel
        : Base.BaseModel
    {
        [DisplayName("Логин")]
        [Remote("CheckLogin", "Account", ErrorMessage = "Такой логин уже существует")]
        [Required(AllowEmptyStrings = false, ErrorMessage = "Логин обязателен для заполнения")]
        [StringLength(15, ErrorMessage = "Логин не должен превышать 15 символов")]
        public string Login { get; set; }

        [DisplayName("Пароль")]
        [Required(AllowEmptyStrings = false, ErrorMessage = "Пароль обязателен для заполнения")]
        [DataType(DataType.Password)]
        [MinLength(6, ErrorMessage = "Пароль должен состоять не менее, чем из 6 символов")]
        [StringLength(255, ErrorMessage = "Пароль слишком длинный(макс 255 символов)")]
        public string Password { get; set; }

        [DisplayName("Подтвердите пароль")]
        [Required(AllowEmptyStrings = false, ErrorMessage = "Подтверждение пароля обязательно.")]
        [System.ComponentModel.DataAnnotations.Compare("Password", ErrorMessage = "Пароль и его подтверждение не совпадают.")]
        [DataType(DataType.Password)]
        public string PasswordConfirm { get; set; }

        [DisplayName("Email")]
        [Required(AllowEmptyStrings = false, ErrorMessage = "Email обязателен для заполнения")]
        [DataType(DataType.EmailAddress)]
        [RegularExpression(@"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", ErrorMessage = "Некорректный адрес")]
        [StringLength(255, ErrorMessage = "Email слишком длинный(макс 255 символов)")]
        public string Email { get; set; }

        [DisplayName("Имя")]
        [StringLength(75, ErrorMessage = "Имя слишком длинное(макс 75 символов)")]
        public string Name { get; set; }

        [HiddenInput(DisplayValue = false)]
        public int AdminId { get; set; }

        [HiddenInput(DisplayValue = false)]
        public int RoleId { get; set; }
    }
}