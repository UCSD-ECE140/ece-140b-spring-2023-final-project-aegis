document.addEventListener('DOMContentLoaded', function () {
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
      
    document.getElementById("sign-out-link").addEventListener("click", function(event) {
        event.preventDefault(); // Prevents the default anchor behavior (navigating to the href)
    
        // Perform the sign-out action or any other desired functionality
        server_request('/logout', {}, 'POST', function(response) {
          if (response.session_id === 0) {
            location.replace('/');
          }
        });
      });
    const profileDropdown = document.querySelector('.profile');
    const menu = document.querySelector('.menu');
  
    profileDropdown.addEventListener('click', function () {
      menu.classList.toggle('hidden');
    });
    
    function deviceScheduleManager() {
        return {
          schedules: [
            {
              id: 1,
              title: 'Morning Configuration',
              startTime: '07:00',
              endTime: '12:00',
              settings: {
                name: 'Morning',
                temp_thresh: '20',
                shielded: 'Yes',
                dongleID: 'Dongle123'
              }
            },
            {
              id: 2,
              title: 'Evening Configuration',
              startTime: '18:00',
              endTime: '23:00',
              settings: {
                name: 'Evening',
                temp_thresh: '18',
                shielded: 'No',
                dongleID: 'Dongle456'
              }
            }
          ],
          newSchedule: {
            id: null,
            title: '',
            startTime: '',
            endTime: '',
            settings: {
              name: '',
              temp_thresh: '',
              shielded: '',
              dongleID: ''
            }
          },
          editingSchedule: null,
      
          addSchedule() {
            this.newSchedule.id = Date.now();
            this.schedules.push({...this.newSchedule});
            this.newSchedule = {
              id: null,
              title: '',
              startTime: '',
              endTime: '',
              settings: {
                name: '',
                temp_thresh: '',
                shielded: '',
                dongleID: ''
              }
            };
          },
      
          editSchedule(schedule) {
            this.editingSchedule = {...schedule};
          },
      
          saveSchedule() {
            let index = this.schedules.findIndex(s => s.id === this.editingSchedule.id);
            if (index !== -1) {
              this.schedules[index] = {...this.editingSchedule};
            }
            this.editingSchedule = null;
          },
      
          deleteSchedule(schedule) {
            this.schedules = this.schedules.filter(s => s.id !== schedule.id);
          },
      
          cancelEditing() {
            this.editingSchedule = null;
          }
        };
      }
      
  });

  