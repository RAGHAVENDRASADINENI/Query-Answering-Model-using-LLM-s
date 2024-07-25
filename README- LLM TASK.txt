Open the LLM_TASK Folder in any IDE- I have use VS Code
The Folder contains three files
1. Dockerfile
2. requirements.txt
3. app.py

make sure u have saved every file in your local 
In VsCode open new terminal and build docker using the command
docker build -t llama-spotify .
after completion run the docker using the command
docker run -p 80:80 llama-spotify
After completion of run open a new terminal and enter your question in the following way
$headers = @{
>>     "Content-Type" = "application/json"
>> }
>> $body = @{
>>     query = "Tell me about the track Sari Konda from the movie Sarkaru Vaari Paata"
>> } | ConvertTo-Json
>> 
>> $response = Invoke-WebRequest -Uri http://localhost/agent -Method POST -Headers $headers -Body $body
>> # Parse the JSON response
>> $responseData = $response.Content | ConvertFrom-Json
>> 
>> # Display the response in a readable format
>> $trackInfo = $responseData.response.tracks.items[0]
>> Write-Host "Track Name: " $trackInfo.name
>> Write-Host "Artist: " $trackInfo.artists[0].name
>> Write-Host "Album: " $trackInfo.album.name
>> Write-Host "Release Date: " $trackInfo.album.release_date
>> Write-Host "Spotify URL: " $trackInfo.external_urls.spotify

Now we will get the ouput in the following format

Track Name:  Sarkaru Vaari Paata-Title Song (From "Sarkaru Vaari Paata")
Artist:  Harika Narayan
Album:  Sarkaru Vaari Paata-Title Song (From "Sarkaru Vaari Paata") - Single
Release Date:  2022-04-24
Spotify URL:  https://open.spotify.com/track/3QY7OcYSIObWfFtYZsvzAx