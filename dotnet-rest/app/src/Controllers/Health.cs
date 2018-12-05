using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Collections.Generic;

namespace web
{
    [Produces("application/json")]
    [Route("v1/{{server_name}}/health")]
    public class Health : Controller
    {
        [HttpGet]
        public IActionResult OnGet()
        {
            var result = new StatusClass
            {
                Status = "OK"
            };
            return Ok(result);
        }
    }

    public class StatusClass
    {
        [JsonProperty(PropertyName = "status")]
        public string Status { get; set; }
    }

}
