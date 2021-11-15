import * as interfaces from './interfaces';

/**
 * Super simple api call to get the text score data
 * Assumes the main.py is running from the wikitrust folder.
 * Expects the api to return json in the format: { words: ['the','brown','fox'], trust_values: [1.5,2,8] }
 * Where the nth word is the nth word in the wikipedia page & the nth trust_value corresponds to the nth word.
 *
 * @returns a promise which resolves with the parsed JSON returned by the API
 *  */
export const fetchScores = (revisionId: number, pageId: number) => {
  // RIGHT NOW We're using revisionId assuming it's unique across all pages. if not, pageId will need to be sent too.
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
          revisionIndex: data.revision_index,
        };
        resolve(output);
      });
    });
};
