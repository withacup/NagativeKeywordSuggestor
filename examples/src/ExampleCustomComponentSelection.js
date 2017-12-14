import React from 'react';
import Gallery from 'react-photo-gallery';
import SelectedImage from './SelectedImage';

class ExampleCustomComponentSelection extends React.Component {
  constructor(props) {
    super(props);
    this.state = { photos: this.props.photos, selectAll: false };
    this.selectPhoto = this.selectPhoto.bind(this);
    this.toggleSelect = this.toggleSelect.bind(this);
  }
  selectPhoto(event, obj){
    let photos = this.state.photos;
    photos[obj.index].selected = !photos[obj.index].selected;
    this.setState({photos: photos});
  }
  toggleSelect(){
    let photos = this.state.photos.map((photo,index)=> { return {...photo, selected: !this.state.selectAll}});
    this.setState({photos: photos, selectAll: !this.state.selectAll});
  }

  handleFormSubmit = formSubmitEvent => {
    formSubmitEvent.preventDefault();

    this.state.photos.map(function(photo, index) {
      if (photo.selected) {
        console.log("image " + index + " selected")
      }
    }
  )};

  render(){
    return (
      <div>
        <h2>Choosing the news source</h2>
        <h3>Ingesting from selected new source to get offensive keywords suggestion</h3>
        <p><button className="toggle-select" onClick={this.toggleSelect}>toggle select all</button></p>
        <form onSubmit={this.handleFormSubmit}>
            <button className="btn btn-default toggle-select" type="submit">Load News</button>       
        </form>
        <Gallery photos={this.state.photos} columns={this.props.columns} onClick={this.selectPhoto} ImageComponent={SelectedImage}/>
      </div>
    );
  }
}

export default ExampleCustomComponentSelection;
