using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using System.Web;
using System.Web.Http;
using System.Net;
using System.Net.Http;
using System.IO;
using System.Threading;
using System.ComponentModel;
using System.Diagnostics;

namespace WebApplicationIC.Controllers
{
    public static class GlobalServer1State
    {
        public static string gameState { get; set; }
        public static string ActionState { get; set; }

        public static Process process { get; set; }

    }
    [Route("game")]
    [ApiController]
    public class ValuesController : ControllerBase
    {
        // GET api/values
        [HttpGet]
        public string Get() //TODO GameStart
        {

            GlobalServer1State.gameState = null;
            GlobalServer1State.ActionState = null;
            return "{\"success\": true}";
        }
        // POST api/values
        [HttpPost]
        public async Task<string> Post([FromBody] string value)
        {
            GlobalServer1State.gameState = value;
            Task<string> result = waitForResponse();

            return await result;
        }
        public static async Task<string> waitForResponse()
        {
            while (GlobalServer1State.ActionState == null)
            {

            }
            string tempActionState = GlobalServer1State.ActionState;
            GlobalServer1State.ActionState = null;
            return tempActionState;
        }
    }

    [Route("frontend")]
    [ApiController]
    public class InfoController : ControllerBase
    {
        // GET: api/Info
        [HttpGet]
        public string Get()
        {
            return GlobalServer1State.gameState;
        }

        // POST: api/Info
        [HttpPost]
        public string Post([FromBody] string value)
        {
            GlobalServer1State.ActionState = value;
            return "{\"success\": true}";
        }
    }
}
