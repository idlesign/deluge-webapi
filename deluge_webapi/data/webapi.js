
WebApiPanel = Ext.extend(Ext.form.FormPanel, {


    constructor: function(config) {

        config = Ext.apply({
            title: _('WebAPI'),
            border: false,
            labelWidth: 10,
            autoHeight: true
        }, config);

        WebApiPanel.superclass.constructor.call(this, config);
    },
    initComponent: function() {
        WebApiPanel.superclass.initComponent.call(this);
        this.opts = new Deluge.OptionsManager();

        var fieldset = this.add({
            xtype: 'fieldset',
            title: _('WebAPI Settings'),
            defaultType: 'checkbox',
            autoHeight: true
        });

        this.opts.bind('enable_cors', fieldset.add({
            name: 'enable_cors',
            id: 'enable_cors',
            height: 22,
            fieldLabel: '',
            labelSeparator: '',
            boxLabel: _('Enable CORS (cross-origin request)')
        }));

        this.list = this.add({
            xtype: 'listview',
            height: 150,
            store: new Ext.data.ArrayStore({
                fields: [
                    { name: 'domain', mapping: 0 }
                ]
            }),
            columns: [{
                id: 'domain',
                header: _('Allowed domain'),
                width: 1,
                sortable: true,
                dataIndex: 'domain'
            }],
            singleSelect: true,
            autoExpandColumn: 'domain',
            listeners: {
                selectionchange: { fn: this.onDomainSelect, scope: this }
            }
        });

        this.panel = this.add({
            region: 'center',
            autoScroll: true,
            items: [this.list]
        });

        this.domain_name = this.opts.bind('domain_name', fieldset.add({
            fieldLabel: '',
            xtype: 'textfield',
            anchor: '50%',
            name: 'domain_name',
            id: 'domain_name',
            autoWidth: true,
            value: ''
        }));

        this.toolbar = this.add({
            fieldLabel: _(''),
            name: 'list_toolbar',
            xtype: 'container',
            layout: 'hbox',
            items: [
                {
                    xtype: 'button',
                    text: 'Add'
                },
                this.domain_name,
                {
                    xtype: 'button',
                    text: 'Remove'
                },
                {
                    xtype: 'button',
                    text: 'Remove all'
                }
            ]
        });

        this.toolbar.getComponent(0).setHandler(this.addDomain, this);
        this.toolbar.getComponent(2).setHandler(this.removeDomain, this);
        this.toolbar.getComponent(3).setHandler(this.removeAllDomain, this);

        deluge.preferences.on('show', this.onPreferencesShow, this);
    },

    removeDomain: function() {
        if (!this.selectedDomain) return;
        var index = this.list.getStore().find('domain', this.selectedDomain);
        if (index == -1) return;
        this.list.getStore().removeAt(index);
        index = this.allowedDomains.indexOf(this.selectedDomain);
        if (index !== -1) this.allowedDomains.splice(index, 1);
        this.selectedDomain = false;
    },

    removeAllDomain: function() {
        this.list.getStore().removeAll();
        this.allowedDomains = [];
        this.selectedDomain = false;
    },

    onDomainSelect: function (dv, selections) {
        if (selections.length === 0) return;
        var r = dv.getRecords(selections)[0];
        this.selectedDomain = r.get('domain');
    },

    addDomain: function() {
        var changed = this.opts.getDirty();
        if (!Ext.isObjectEmpty(changed)) {
            if (!Ext.isEmpty(changed['domain_name'])) {
                changed['domain_name'] = changed['domain_name'];
                this.allowedDomains.push(changed['domain_name']);
                this.updateDomainsGrid();
            }
        }
    },

    updateDomainsGrid: function () {
        var Domains = [];
        Ext.each(this.allowedDomains, function (domain) {
                Domains.push([domain]);
        }, this);
        this.list.getStore().loadData(Domains);
    },

    onPreferencesShow: function () {
        deluge.client.webapi.get_config({
            success: function (config) {
                if (!Ext.isEmpty(config['enable_cors'])) {
                    config['enable_cors'] = config['enable_cors'];
                }
                if (!Ext.isEmpty(config['allowed_origin'])) {
                    config['allowed_origin'] = config['allowed_origin'];
                }
                this.allowedDomains = config['allowed_origin'];
                this.updateDomainsGrid();
                this.opts.set(config);
            },
            scope: this
        });
    },

    onApply: function(e) {
        var changed = this.opts.getDirty();
        if (!Ext.isObjectEmpty(changed)) {
            if (!Ext.isEmpty(changed['enable_cors'])) {
                changed['enable_cors'] = changed['enable_cors'];
            }
            deluge.client.webapi.set_config(changed, {
                success: this.onSetConfig,
                scope: this
            });
        }
        var config = {};
        config['allowed_origin'] = this.allowedDomains;
        console.log(config);
        deluge.client.webapi.set_config(config);
    },

    onSetConfig: function() {
        this.opts.commit();
    }

});


WebApiPlugin = Ext.extend(Deluge.Plugin, {

    name: 'WebAPI',

    onDisable: function() {
        deluge.preferences.removePage(this.prefsPage);
    },

    onEnable: function() {
        this.prefsPage = deluge.preferences.addPage(new WebApiPanel());
    }
});

Deluge.registerPlugin('WebAPI', WebApiPlugin);