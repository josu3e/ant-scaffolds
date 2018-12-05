FROM  microsoft/dotnet-nightly:2.1-runtime-alpine

COPY ./app/release /app
WORKDIR /app

ENTRYPOINT ["dotnet", "app.dll", "--server.urls", "http://*:80"]