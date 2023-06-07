document.addEventListener('DOMContentLoaded', function() {
    function server_request(url, data = {}, verb, callback) {
        return fetch(url, {
          credentials: 'same-origin',
          method: verb,
          body: JSON.stringify(data),
          headers: { 'Content-Type': 'application/json' }
        })
          .then(response => response.json())
          .then(response => {
            if (callback)
              callback(response);
          })
          .catch(error => console.error('Error:', error));
      }

      
  });
  