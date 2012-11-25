Pages = { //model
	'data':null,
	'getPage' : function(name) {
		if(this.is_empty())
			this.refresh();
		return this.data[name];
	},
	'getPages': function() {
			return Object.keys(this.data);
	},
	'hasPage': function(name) {
		var page = this.data[name];
		return !(page==undefined);
	},
	'is_empty' : function() {
		if(this.data==null)
			return true;
		return false;
	},
	'_sendPage' : function (name, content, create) {
		if(create==true) {
			method='POST';
			url = 'page/';
		}
		else {
			method='PUT';
			url = 'page/' + name;
		}

		$.ajax({
			url: url,
			type: method,
			data: {slug: name, content: content},
			success: function(result) {
				$(Pages).trigger('save_success', {name: name, type:create ? "create" : "edit"});
			}
			//TODO: failure
		});

		this.data[name] = content;
	},
	'deletePage' : function (name) {
		$.ajax({
			url: 'page/' + name,
			type: 'DELETE',
			success: function(result) {
				$(Pages).trigger('save_success', {name: name, type:'delete'});
			}
			//TODO: failure
		});

		delete this.data[name];
	},
	'setPage': function(name, content) {
		this._sendPage(name, content, false);
	},
	'addPage': function(name, content) {
		this._sendPage(name, content, true);
	},
	'refresh' : function() {}, //TODO: get /pages
	'getDefaultPage' : function() {
		var page = this.data['main'];
		if(page==undefined)
			return Object.keys(this.data)[0];
		return 'main';
	}
};
var View = function(elem, model) {
	this.elem = elem;
	this.model = model;
	this.mode = 0; //0 is for read, 1 is for edit
	this.currentpage = model.getDefaultPage();
	this.conv = new Markdown.getSanitizingConverter();
	var ed = new Markdown.Editor(this.conv);
	this.conv.hooks.chain("postConversion", function (text) {
			return text.replace(/\[\[([a-z_]*)\]\]/gi, '<a href="#$1">$1</a>');
	});
	ed.run();
	var thisview = this;
	$('#submit', this.elem).click(function() {
		console.log('user wants to submit');
		$(thisview).trigger('page-submit');
	});
}
View.prototype.refresh = function() {
	var page = this.model.getPage(this.currentpage);
	if(page == undefined)
		page = "# " + this.currentpage + "\n\nHey, I'm a **new** page; write your text here. This is a link to [[main]] page";
	$('#content', this.elem).html(this.conv.makeHtml(page));
	$('#wmd-input').val(page);
	if(this.mode == 0) {
		$('#content', this.elem).show();
		$('#editor', this.elem).hide();
	} else {
		$('#content', this.elem).hide();
		$('#editor', this.elem).show();
	}
}
View.prototype.getEditorContent = function() {
	return $('#wmd-input', this.elem).val();
}
View.prototype.goto_page = function(name) {
	if(arguments.length==0)
		this.currentpage = this.model.getDefaultPage();
	else
		this.currentpage = name;
	this.refresh();
}
View.prototype.goto_404 = function(name) {
	this.mode = 1;
	this.currentpage = name;
	this.refresh()
}
View.prototype.switch_mode = function(mode) {
	if(arguments.length==0)
		this.mode = !this.mode;
	else {
		if(mode==1 || mode == 'edit')
			this.mode = 1;
		else
			this.mode = 0;
	}
	this.refresh()
}

NavView = function(rootelem,  model) {
	this.model = model;
	this.elem = rootelem;
	this.refresh()
}
NavView.prototype.refresh = function() {
	$('#pagelist > li', this.elem).remove();
	for(var i=0; i<Pages.getPages().length; i++) {
		name = Pages.getPages()[i];
		$('#pagelist', this.elem).append('<li><a href="#' + name + '">' + name + '</a></li>');
	}
}

Controller = function() {
	this.view = new View($('#page'), Pages);
	this.navView = new NavView($('#nav'), Pages);
	var thisapp = this;
	$(Pages).bind('save_success', function(evt, data) {
		if(data['type'] == 'create' || data['type'] == 'delete') {
			thisapp.navView.refresh();
			if(data['type'] == 'delete' && data['name'] == thisapp.view.currentpage)
				thisapp.change_page();
		}
	}); //TODO: use a notification
	$(this.view).bind('page-submit', function() {
		newcontent = app.view.getEditorContent();
		console.log("submitting..."); //TODO: use a notification
		if(Pages.hasPage(app.view.currentpage))
			Pages.setPage(app.view.currentpage, newcontent);
		else
			Pages.addPage(app.view.currentpage, newcontent);
		thisapp.change_mode();
	});
}
Controller.prototype.change_page = function(name) {
	if(arguments.length == 0)
		name = Pages.getDefaultPage();
	window.location.hash = name;
	if(Pages.hasPage(name))
		this.view.goto_page(name);
	else
		this.view.goto_404(name);
}
Controller.prototype.change_mode = function() {
	this.view.mode = !this.view.mode;
	this.view.refresh();
}
$(function() {
	//TODO: make better nav in NavView
	app = new Controller();
	if(window.location.hash == "")
		app.change_page();
	else
		app.change_page(window.location.hash.substring(1));
	window.addEventListener('hashchange', function(){
	  app.change_page(window.location.hash.substring(1));
	})

	$('#mode-switch').click(function() {//FIXME: event launched by the NavView to the controller
		app.change_mode()
	});
});

// vim: set fdm=indent:
