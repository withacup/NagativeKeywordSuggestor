const express = require('express');
const router = express.Router();
const data = require("../data");
const events = data.events;
const locations = data.locations;
const people = data.people;

// Single Event Page
router.get("/:id", (req, res) => {
    // Find a event by the provided id, 
    // then display its information
    // As well as listing the names of all the attendees that will be at this event 
    // Each of these attendee names will need to link to their person page
    // You will also list the location of the event, said location's name, and a link to the location page
    events.getEvent(req.params.id).then(event => {
        // console.log(event);
        return people.getAllPeople().then(allPeople => {
            locations.getLocation(event.location).then(location => {
                let attend = allPeople.filter(function(p) {
                    return event.attendees.indexOf(p.id) >= 0;
                });
                res.render('events/single', {event: event, attend: attend, locationName: location.name});
            })
        })
    }).catch(err => {
        console.log(err);
        res.redirect("http://localhost:3000/public/404.html");
    })
    // If a event is not found, display the 404 error page
    // res.render("/misc/debug", { debug: true, modelData: { something: "SomeValue" } });
});

// Event Index Page
router.get("/", (req, res) => {
    // Display a list of all events; it can be in an unordered list, or a table
    // Each of these events need to link to the single event page
    events.getAllEvents().then(allEvents => {
        res.render('events/list', {allEvents: allEvents});
    })
    .catch(err => {
        console.log(err);
        res.redirect("http://localhost:3000/public/404.html");
    })
    // res.render("/misc/debug", { debug: true, modelData: { something: "SomeValue" } });
});

module.exports = router;