#!/usr/bin/env python3
"""
GitHub Data Collector for Ecosystem Health Index

This script collects publicly available data from GitHub to assess
the developer engagement and activity metrics for the EHI.
"""

import os
import json
import time
import argparse
import pandas as pd
from datetime import datetime, timedelta
from github import Github, RateLimitExceededException

class GitHubCollector:
    """Collects GitHub metrics for ecosystem health assessment."""
    
    def __init__(self, token=None):
        """Initialize the GitHub collector with optional token."""
        self.g = Github(token) if token else Github()
        self.metrics = {
            "repo_count": 0,
            "total_stars": 0,
            "total_forks": 0,
            "total_issues": 0,
            "total_prs": 0,
            "contributor_count": 0,
            "commit_frequency": 0,
            "response_time_avg": 0,
            "issue_close_rate": 0,
            "recent_activity_score": 0
        }
        self.raw_data = {}
    
    def collect_organization_data(self, org_name, days_back=90):
        """Collect data for an entire GitHub organization."""
        try:
            org = self.g.get_organization(org_name)
            repos = org.get_repos(type="public")
            
            # Store organization-level data
            self.raw_data["organization"] = {
                "name": org.name,
                "url": org.html_url,
                "repos": [],
                "collected_at": datetime.now().isoformat()
            }
            
            # Process each repository
            for repo in repos:
                self._process_repository(repo, days_back)
            
            # Calculate aggregate metrics
            self._calculate_metrics()
            
            return self.metrics
            
        except RateLimitExceededException:
            wait_time = self.g.get_rate_limit().core.reset - datetime.now()
            print(f"Rate limit exceeded. Reset in {wait_time}")
            raise
        except Exception as e:
            print(f"Error collecting data for organization {org_name}: {str(e)}")
            raise
    
    def _process_repository(self, repo, days_back):
        """Process a single repository."""
        # Skip forks, archived, or empty repos
        if repo.fork or repo.archived or repo.size == 0:
            return
        
        # Basic repo data
        repo_data = {
            "name": repo.name,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat()
        }
        
        # Get recent commits
        since_date = datetime.now() - timedelta(days=days_back)
        try:
            commits = list(repo.get_commits(since=since_date))
            repo_data["recent_commit_count"] = len(commits)
        except Exception:
            repo_data["recent_commit_count"] = 0
        
        # Get contributors
        try:
            contributors = list(repo.get_contributors())
            repo_data["contributor_count"] = len(contributors)
        except Exception:
            repo_data["contributor_count"] = 0
        
        # Get recent PRs and calculate response time
        try:
            pulls = list(repo.get_pulls(state='all', sort='created', direction='desc'))
            recent_pulls = [p for p in pulls if p.created_at > since_date]
            repo_data["recent_pr_count"] = len(recent_pulls)
            
            # Calculate average time to first review
            review_times = []
            for pr in recent_pulls[:10]:  # Limit to latest 10 for performance
                if pr.created_at and pr.updated_at:
                    review_times.append((pr.updated_at - pr.created_at).total_seconds() / 3600)
            
            repo_data["avg_review_time_hours"] = sum(review_times) / len(review_times) if review_times else None
        except Exception:
            repo_data["recent_pr_count"] = 0
            repo_data["avg_review_time_hours"] = None
        
        # Store repo data
        self.raw_data["organization"]["repos"].append(repo_data)
    
    def _calculate_metrics(self):
        """Calculate aggregate metrics from raw data."""
        repos = self.raw_data["organization"]["repos"]
        if not repos:
            return
        
        # Basic counts
        self.metrics["repo_count"] = len(repos)
        self.metrics["total_stars"] = sum(r["stars"] for r in repos)
        self.metrics["total_forks"] = sum(r["forks"] for r in repos)
        self.metrics["total_issues"] = sum(r["open_issues"] for r in repos)
        self.metrics["total_prs"] = sum(r.get("recent_pr_count", 0) for r in repos)
        
        # Contributor metrics
        contributors = sum(r.get("contributor_count", 0) for r in repos)
        self.metrics["contributor_count"] = contributors
        
        # Commit frequency
        commits = sum(r.get("recent_commit_count", 0) for r in repos)
        days_period = 90  # Assuming default 90 days
        self.metrics["commit_frequency"] = commits / days_period if days_period > 0 else 0
        
        # Response time average
        response_times = [r.get("avg_review_time_hours", 0) for r in repos if r.get("avg_review_time_hours") is not None]
        self.metrics["response_time_avg"] = sum(response_times) / len(response_times) if response_times else 0
        
        # Calculate recent activity score (custom metric)
        # Formula: (commits + PRs) / days * log(stars + 1)
        activity = (commits + self.metrics["total_prs"]) / days_period
        star_factor = sum(min(1 + r["stars"], 1000) for r in repos) / len(repos)
        self.metrics["recent_activity_score"] = activity * star_factor / 100
    
    def save_data(self, output_path):
        """Save collected data to a JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump({
                "raw_data": self.raw_data,
                "metrics": self.metrics,
                "collected_at": datetime.now().isoformat()
            }, f, indent=2)
        print(f"Data saved to {output_path}")
    
    def to_dataframe(self):
        """Convert metrics to a pandas DataFrame."""
        df = pd.DataFrame([self.metrics])
        return df


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Collect GitHub metrics for EHI analysis')
    parser.add_argument('organization', help='GitHub organization name')
    parser.add_argument('--token', help='GitHub API token')
    parser.add_argument('--days', type=int, default=90, help='Days back to analyze')
    parser.add_argument('--output', default='data/github_metrics.json', help='Output file path')
    
    args = parser.parse_args()
    
    collector = GitHubCollector(token=args.token)
    
    try:
        metrics = collector.collect_organization_data(args.organization, days_back=args.days)
        collector.save_data(args.output)
        print(f"Collected metrics for {args.organization}:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
