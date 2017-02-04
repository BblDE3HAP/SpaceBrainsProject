﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using BusinessLogic.DTO;
using BusinessLogic.Services.Base;
using DataAccess.Repositories.Base;
using AutoMapper;
using Domain.Entities;

namespace BusinessLogic.Services
{
    public class CrawlerStatsService :
        Base.ICrawlerStatsService
    {
        ICrawlerRepository crawlerRepository = null;

        public CrawlerStatsService(ICrawlerRepository crawlerRepository)
        {
            this.crawlerRepository = crawlerRepository;
        }
        public IEnumerable<CrawlerStatsDTO> GetCrawlerStats()
        {
            List<CrawlerStatsDTO> stats = new List<CrawlerStatsDTO>();
           
            var sites = GetSites();
            foreach (SiteDTO s in sites)
            {
                CrawlerStatsDTO statsobj = new CrawlerStatsDTO();
                IEnumerable<PageDTO> pages = GetAllPagesForSite(s.Id);
                int countAll = 0;
                int countVisited = 0;
                int countnotVisited = 0;
                foreach (PageDTO p in pages)
                {
                    countAll++;
                    if (p.LastScanDate == null)
                    {
                        countnotVisited++;
                    }
                    else
                    {
                        countVisited++;
                    }
                }
                statsobj.Site = s.Name;
                statsobj.SiteId = s.Id;
                statsobj.CountAllLinks = countAll;
                statsobj.CountNotVisitedLinks = countnotVisited;
                statsobj.CountVisitedLinks = countVisited;
              stats.Add(statsobj);
            }
            
            return stats;
        }

      
        public IEnumerable<SiteDTO> GetSites()
        {
            var sites = crawlerRepository.GetSites();

            Mapper.Initialize(cfg => cfg.CreateMap<Site, SiteDTO>()
               .ForMember(dest => dest.Url, opt => opt.Ignore()));
            return Mapper.Map<IEnumerable<Site>, IEnumerable<SiteDTO>>(sites);
        }

        public IEnumerable<PageDTO> GetAllPagesForSite(int id)
        {
            var pages = crawlerRepository.GetAllPagesForSite(id);
            Mapper.Initialize(cfg => cfg.CreateMap<Page, PageDTO>());
            return Mapper.Map<IEnumerable<Page>, IEnumerable<PageDTO>>(pages);
        }

    }
}
