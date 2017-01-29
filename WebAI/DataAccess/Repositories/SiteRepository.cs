﻿using DataAccess.Context;
using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Linq.Expressions;
using System.Data.Entity;
using DataAccess.Repositories.Base;
namespace DataAccess.Repositories
{
    public class SiteRepository
        : ISiteRepository
    {
        WebAIDbContext context;

        public SiteRepository(WebAIDbContext context)
        {
            this.context = context;
        }

        

        public void AddSite(Site site, string url)
        {
            if (site != null)
            {
                context.Sites.Add(site);
                context.SaveChanges();

                context.Pages.Add(new Page { Url = url, SiteId = site.Id, FoundDateTime = DateTime.Now });
                context.SaveChanges();
            }
        }

        

        public void ChangeSite(Site site)
        {
            if (site == null)
                return;
            context.Entry(site).State = System.Data.Entity.EntityState.Modified;
            context.SaveChanges();
        }

        
       

        public void DeleteSiteById(int id)
        {
            //????? каскадное удаление
            Site site = context.Sites
                .Include(x => x.Pages)
                .Include(x => x.Pages.Select(y => y.Ranks))
                .FirstOrDefault(x => x.Id == id);
            if (site == null)
                return;
            context.Sites.Remove(site);
            context.SaveChanges();
        }

        

        public IEnumerable<Site> GetSites()
        {
            return context.Sites.ToArray();
        }

        

        public Site GetSite(int id)
        {
            return context.Sites.FirstOrDefault(x => x.Id == id);
        }
        public IEnumerable<Page> GetAllPagesForSite(int id)
        {
            return context.Pages.Where(x => x.SiteId == id).ToArray();
        }
    


}


}
