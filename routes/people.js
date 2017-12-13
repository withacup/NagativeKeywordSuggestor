const express = require('express');
const router = express.Router();
const data = require("../data");
const path = require('path');
const people = data.people;
const events = data.events;
// Single Person Page
router.get("/:id", (req, res) => {
    // Find a person by the provided id, 
    // then display their information
    // As well as listing all events that they will be attending
    // Each of these events need to link to the event page, and show the event name
    // If a person is not found, display the 404 error page
    people.getPerson(req.params.id)
    .then(person => {
    	events.getEventsForAttendee(person.id)
        .then(eventsList => {
    		console.log(eventsList);
	    	res.render('people/single', {people: person, eventsList: eventsList});
    	})
    }, (err) => {
        console.log(err);
        res.redirect("http://localhost:3000/public/404.html");
    })
});

// People Index Page
router.get("/", (req, res) => {
    // Display a list of all people; it can be in an unordered list, or a table
    // Each of these people need to link to the single person page
    people.getAllPeople().then(listOfPeople => {
    	res.render('people/list', {listOfPeople: listOfPeople});
    })
});

router.get('events/:id', (req, res) => {
    events.getEvent(req.params.id).then(event => {
        return people.getAllPeople().then(allPeople => {
            console.log(allPeople);
            let attend = allPeople.filter(function(p) {
                return event.attendees.indexOf(p.id) >= 0;
            });
            res.render('events/single', {event: event, attend: attend});
        })
    }).catch(err => {
        console.log(err);
        res.redirect("http://localhost:3000/public/404.html");
    })
})


module.exports = router;