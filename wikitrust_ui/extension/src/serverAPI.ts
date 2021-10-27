import * as interfaces from './interfaces';

/**
 * Super simple api call to get the text score data
 * Assumes the api_demo.py is running from the algorithims analysis folder.
 * Expects the api to return json in the format: { Words: ['the','brown','fox'],Scores: [1.5,2,8]}
 * Where the Nth word is the nth word in the wikipedia page & the nth score corresponds to the nth word.
 *
 * @returns a promise which resolves with the parsed JSON returned by the API
 *  */
export const fetchScores = (revisionId: number, pageId: number) => {
  return fetch(
    'http://localhost:8000/api?action=get_revision_text_trust&revision_id=' +
      revisionId
  )
    .then((response) => response.json())
    .then((data) => {
      return new Promise<interfaces.serverScoresResponse>((resolve, reject) => {
        console.log(
          'Got revision (' + revisionId + ') text trust from server: ',
          data
        );
        if (data['error']) {
          console.warn('Server Error: ' + data['error']);
          reject('Server Error: ' + data['error']);
        }
        const output: interfaces.serverScoresResponse = {
          words: data.words,
          scores: data.trust_values,
        };
        resolve(output);
      });
    });
};
