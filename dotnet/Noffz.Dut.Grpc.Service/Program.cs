using Noffz.Dut.Grpc.Service;
using Noffz.Dut.Grpc.Service.Services;

// ContentRootPath = exe folder so appsettings.json is found when running as a
// Windows Service (whose working directory is System32).
var builder = WebApplication.CreateBuilder(new WebApplicationOptions
{
    Args = args,
    ContentRootPath = AppContext.BaseDirectory,
});

// No-op unless started by the Windows Service Control Manager.
builder.Host.UseWindowsService(o => o.ServiceName = "NoffzDutControl");

builder.Services.Configure<DutOptions>(builder.Configuration.GetSection(DutOptions.Section));
builder.Services.AddSingleton<DutSession>();
builder.Services.AddGrpc(o => o.EnableDetailedErrors = true);
builder.Services.AddGrpcReflection();   // lets grpcurl / Postman discover the API

var app = builder.Build();

app.MapGrpcService<DutControlService>();
app.MapGrpcReflectionService();

app.Services.GetRequiredService<DutSession>().TryAutoOpen();

app.Run();
