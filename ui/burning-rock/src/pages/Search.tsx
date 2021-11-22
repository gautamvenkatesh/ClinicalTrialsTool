/**
 * Search page for trials
 */
/**
 * Search page for trials
 */
 import React from 'react'
 import { Dropdown, Form } from 'semantic-ui-react'


 const SORT_TYPES = ["Start Date", "nci_id", "Relevance"]
 const STATUS_FILTERS = [""]
 

 const DropdownMenu = (name:string , options: Array<{}>) => (
    <Dropdown
        placeholder={name}
        fluid
        multiple
        search
        selection
        options={options}
    />
    )
 

 
 const Search: React.FC = () => {
 return (
     <>
 
     <Form>
        <div className="field"> 
            <label>Keywords</label>
        </div>
    
        {DropdownMenu('sort type', )}
 
 
     </Form>
 
 
 
 
     </>
 );
 }
 
 
 {/* <form class="ui form">
   <div class="field">
     <label>First Name</label>
     <input type="text" name="first-name" placeholder="First Name">
   </div>
   <div class="field">
     <label>Last Name</label>
     <input type="text" name="last-name" placeholder="Last Name">
   </div>
   <div class="field">
     <div class="ui checkbox">
       <input type="checkbox" tabindex="0" class="hidden">
       <label>I agree to the Terms and Conditions</label>
     </div>
   </div>
   <button class="ui button" type="submit">Submit</button>
 </form> */}
 
 export default Search;
 




