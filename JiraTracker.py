#!/usr/bin/env python3
import logging

class JiraTracker(object):
    def __init__(self,clients):
        self.clients=clients

    def listallissues(self,release):
        self.release=release
        self.issues=self.clients.jira.search_issues('fixVersion='+self.release)
        self.issuekeys=['{}'.format(self.issue.key) for self.issue in self.issues]
        logging.info('Tickets for release %s: %s',release,self.issuekeys)
        return(self.issuekeys)

    def get_issuelog(self,issuekey):
        self.chlog=self.clients.jira.issue(issuekey, expand='changelog')
        return(self.chlog)

    def get_transitionlog(self,issuekeys):
        self.transdict={}
        for issuekey in issuekeys[:]:
            self.statusdict.setdefault(issuekey,[])
            logging.debug('Get transition log for %s',issuekey)
            for history in self.get_issuelog(issuekey).changelog.histories:
                for item in history.items:
                    if(item.field=='status'):
                        if(issuekey in self.statusdict):
                            self.statusdict[issuekey].append(item.toString)
                        else:
                            self.statusdict[issuekey]=[item.toString]
        logging.debug('Issues and their status %s',self.statusdict)
        return(self.transdict)

    def checkstatus(self,issuekeys,status):
        self.status=status
        self.statusdict={}
        for issuekey in issuekeys[:]:
            self.sts=str(self.clients.jira.issue(issuekey).fields.status)
            self.istype=str(self.clients.jira.issue(issuekey).fields.issuetype)
            if(self.sts==status):
                logging.debug('%s is in %s state',issuekey,status)
                issuekeys.remove(issuekey)
            elif((self.istype!='Story') and (status=='Done') and (self.sts in ['Closed','Resolved'])):
                logging.debug(('%s is in % state',issuekey,status))
                issuekeys.remove(issuekey)
            else:
                self.statusdict[issuekey]=self.sts
        logging.debug('Invalid tickets and their status %s',self.statusdict)
        return(self.statusdict)










