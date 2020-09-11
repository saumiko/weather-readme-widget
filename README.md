
<p align="center">
 <img width="100px" src="https://raw.githubusercontent.com/saumiko/weather-readme-widget/master/icon.svg" align="center" alt="GitHub Readme Stats" />
 <h2 align="center">GitHub Readme Weather Stats</h2>
 <p align="center">Get dynamically generated weather stats on your GitHub readmes!</p>

  <p align="center"><a href="https://weather-readme.vercel.app/api/weather"><img alt="Powered by Vercel" src="https://raw.githubusercontent.com/saumiko/weather-readme-widget/master/vercel.svg" /></a></p>
  <p align="center">
    <a href="#demo">View Demo</a>
    ·
    <a href="https://github.com/saumiko/weather-readme-widget/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/saumiko/weather-readme-widget/issues/new/choose">Request Feature</a>
  </p>
  
## Demo
[<img align="top" src="https://weather-readme.vercel.app/api/weather" alt="Weather" width="100%"/>](https://openweathermap.org/city/1185098)

Demo URL: `https://weather-readme.vercel.app/api/weather`


## Workflow 
This app is basically written with Vercel deployment plan in mind. Since I had issues with reading the configuration after deployment, decided to load the configuration from the repository itself.
Tried to maintain standard! You can change it if you want some kind of different loading strategy.
The weather data & icons are pulled from [OpenWeather](https://openweathermap.org), each time the widget gets loaded. 
For time adjustments, UTC adjustments are done according to the Vercel instance. So it may behave wierdly in local.
The API key for [OpenWeather](https://openweathermap.org), is supplied by an environment variable named `OPENWEATHERMAP`.
Calculations & adjustments are done and the [widget](https://github.com/saumiko/weather-readme-widget/blob/master/api/templates/widget.html) template is rendered as a vector image in the final output for the [weather](https://weather-readme.vercel.app/api/weather) api.

## Deploy on your own Vercel instance

1. Configure your repository
	- [Fork my repository](https://github.com/saumiko/weather-readme-widget/fork)
	- [Edit the configurations](https://github.com/saumiko/weather-readme-widget/blob/master/api/config.ini)
		 - [ ] [Location Dict](https://github.com/saumiko/weather-readme-widget/blob/dac00febabee2bc9c406cf78aa4a92ca7088333f/api/config.ini#L7)
		 - [ ] [Timezone Dict](https://github.com/saumiko/weather-readme-widget/blob/dac00febabee2bc9c406cf78aa4a92ca7088333f/api/config.ini#L12)
	- [Edit GitHub info](https://github.com/saumiko/weather-readme-widget/blob/dac00febabee2bc9c406cf78aa4a92ca7088333f/api/weather.py#L14)
		 - [ ] `GITHUB_USERNAME`
		 - [ ] `GITHUB_REPO`
		 - [ ] `GIT_BRANCH`
	- Push updates in your fork!

2. Configure Vercel instance & deploy!
	- Sign up!
	- Connect & deploy your repository!
		- [ ] Just add your own `appid` for openweathermap api in `OPENWEATHERMAP` env variable.
	- Voila! It'll be up and running after that!
		- Access path - `http://VERCEL_DOMAIN/api/weather`

## Contributions & License
This app is licensed under MIT License. ©[Asif Mohaimen](https://asifmohai.men), 2020

Contributions are welcome! Please send your PR!

Made with  ❤️!