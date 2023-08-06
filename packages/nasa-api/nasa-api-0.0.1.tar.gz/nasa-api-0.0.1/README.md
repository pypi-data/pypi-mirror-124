# NASA-API
`nasa-api` is an async wrapper for The Official NASA API.

Note: Currently in development.

Make sure to generate an API key from https://api.nasa.gov/

## Available APIs

### APOD
Stands for `Astronomy Picture of the Day`.

```py
import nasa
import asyncio

async def main():
    response = await nasa.APOD().apod('API-KEY-HERE', **kwargs)   
    print(response)

asyncio.get_event_loop().run_until_complete(main())
```

Parameters:
|Parameter|	Type|	Example | Description|
|---------|-------|------| ---------|
|date	| `str` |	`"YYYY-MM-DD"`, `"2021-06-11"`|	The date of the APOD image to retrieve|
|date_range| `str`|	`"START_DATE, END_DATE"`, `"YYYY-MM-DD, YYYY-MM-DD"`, `"2021-06-11, 2021-07-30"`| A date range, when requesting date for a range of dates. Cannot be used with `date`.|
|count| `int` |	`1` | If this is specified then count randomly chosen images will be returned. Cannot be used with `date` or `date_range`.|
|thumbs|	str | `"True"`, `"False"`|	Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored.|
|api_key| `str`	| `"DEMO_KEY"`	| a api.nasa.gov key. This is a positional argument|