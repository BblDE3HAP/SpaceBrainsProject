﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebAI.Models
{
    public class SiteViewModel
        : Base.BaseModel
    {
        public string Name { get; set; }
        public string Url { get; set; }
    }
}