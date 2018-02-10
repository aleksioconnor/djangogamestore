// ** Contains javascript for the gameview page ** //

// Adds event listener to window, which will monitor any incoming messages
// from the iFrame
window.addEventListener('message', function (message) {
  switch (message.data.messageType) {

    // If message type is score, save high score
    case "SCORE":
      saveHighScore(message.data.score)
      break;

    // If message type is save, save game state
    case "SAVE":
      saveGameState(message.data.gameState);
      break;

    // If message type is load request, load game
    case "LOAD_REQUEST":
      requestLoad();
      break;

    // TODO: Add error handling.
    case "ERROR":
      break;

    // change the size of the iframe according to options received from iFrame
    case "SETTING":
      var gameframe = $('#gameframe')
      gameframe.css('height', message.data.options.height + 'px');
      gameframe.css('width', message.data.options.width + 'px');
      gameframe.css('background-color', 'white');
      break;
  }
});

  // Get csrf token. csrf variable is specified in the gameview template.
  var token = $(csrf).val();

/**
 * @param { object }
 *
 * Function changes javascript object to string and sends it to
 * the endpoint 'state' to save the game state. See /gameview/views for
 * details.
 */

  function saveGameState(state) {
    var data = JSON.stringify(state);

    $.ajax({
      type: "POST",
      data: {
        'state': data,
        'csrfmiddlewaretoken': token,
      },
      url: "state/",
      success: function (result) {
        // TODO: Send message to iframe, and handle error
      }
    });
  }

/**
 * @param { int }
 *
 * Function sends score to 'score' endpoint. See /gameview/views for details.
 */
  function saveHighScore(score) {
    $.ajax({
      type: "POST",
      data: {
        'score': score,
        'csrfmiddlewaretoken': token,
      },
      url: "score/",
      success: function (result) {
        getHighScores()
        // TODO: Send message to iframe, and handle errors
      }
    })
  }

/**
 * Function requests newest save from 'load' endpoint.
 *
 */
  function requestLoad() {
    $.ajax({
      type: "GET",
      url: "load/",
      success: function (result) {
          var json = parseJson(result);

          // Hacky fix to return the message to json format
          var gameState = parseJson(json[0].fields.state)
          var iframe = $('#gameframe')[0]
          var message = {};

          message.messageType = "LOAD";
          message.gameState = gameState;

          iframe.contentWindow.postMessage(message, "*");
        },
      error: function(result) {
        // Messages should be handled in views i guess?
        var iframe = $('#gameframe')[0]

        var message = {};
        message.messageType = "ERROR";
        message.info = "No saved games found";
        iframe.contentWindow.postMessage(message, "*");
        
      }
    })
  }

  function getHighScores() {
    $.ajax({
      type: "GET",
      url: "scores/",
      success: function(result) {
        $('#scores').empty()
        $.each(result, function(i, n) {
          $('#scores').append(n.player + ": " + n.score + "<br>")
        })
      }
    })
  }

  function iframeMessage(message) {
    var iframe = $('#gameframe');
    if (iframe) {
      iframe.contentWindow.postMessage(message)
    }
  }

  function parseJson(data) {
    var json = JSON.parse(data);
    return json;
  }

// Document ready for retrieving high scores
$(document).ready(function(){
  getHighScores();
})
