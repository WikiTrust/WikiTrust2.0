/**
 * Super simple api call to get the text score data
 * Assumes the api_demo.py is running from the algorithims analysis folder.
 * Expects the api to return json in the format: { Words: ['the','brown','fox'],Scores: [1.5,2,8]}
 * Where the Nth word is the nth word in the wikipedia page & the nth score corresponds to the nth word.
 *
 * @returns a promise which resolves with the object representation of the parsed JSON returned by the API
 *  */
export const fetchScores = () => {
  const h = setTimeout(() => {
    alert(
      'Make sure you are running the api_demo.py in the algorithims analysis folder (it only works on the lady gaga meat dress or World Health Organization pages). You can download the code from the Slack.'
    );
  }, 3000);
  return fetch('http://localhost:8080').then(response => {
    clearTimeout(h);
    return response.json();
  });
};
