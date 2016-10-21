import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

import './loading.html';

setTimeout(toResults, 5000);
	
function toResults() {
	location.href="/results";
}

