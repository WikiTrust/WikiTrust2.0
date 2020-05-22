# Database and Algorithm Workflow
The tables in our database are laid out below, followed by an explanation of the workflow between them and the algorithms

## Tables
##### environment
An environment is a set of pages with similar subject matter, such that an author has the same reputation on all of them. An edit on one page in an environment affects the reputation not only on that page, but on all pages in the environment. Each environment has a unique *environment_id*, along with plain text *environment_name*. Some examples are "Medicine", "Politics", etc... We assume that there is no overlap between environments.

##### page
A page in the table corresponds to a page on Wikipedia. 

Fields:
 - *page_id*: Wikipedia Page ID
 - *page_title*: Wikipedia Page Title
 - *page_environment*: A reference to the Environment the page is a part of
 - *analysis_start_time*: The date and time at which pages are considered for analysis

The *analysis_start_time* is the date and time at which analysis begins. In other words, only revisions made later or on that date are analyzed. 

##### revision
A revision in the table corresponds to a revision of a page on Wikipedia. 

Fields:
 - *revision_id*: Wikipedia Revision ID
 - *user*: A reference to the user who made the revision
 - *rev_date*: The date and time the revision was made
 - *rev_page*: A reference to the page this revision is a part of
 - *rev_file_name*: The name of the compressed file containing this revision in GCS
 - *rev_file_offset*: The offset in the compressed file where this revision is stored.
 - *annotation_date*: The date at which the text trust annotation was last computed for this revision.

We do not store the location of the annotated trust data because we plan to store this statically using a CDN.

##### user_reputation
The reputation of a user in a certain environment.

Fields:
 - *user*: A reference to the user in question
 - *environment*: A reference to the environment in which this reputation is in scope
 - *reputation*: The reputation of the user in the environment

##### edit_distance
A cache of computed edit distances.

Fields:
-*revision_id_1*: The origin revision id
-*revision_id_2*: The destination revision id
-*edit_distance*: The edit distance between the two revision ids

Note that revision_id_1 should be less than revision_id_2.

## Workflow
The workflow begins with the designation of a new page being added. The page and environment tables are updated, and the page name passed to the revision puller. The revision puller begins pulling revisions, compressing them, and storing them in the GCS. The revision puller continuously updates the revision table with the information related to new revisions.

 At this point we now have the option of calling the author reputation algorithms to populate the edit_distance table. Recall the constant _m_ from the paper "Robust Content-Driven Reputation" 2.2. We select a value _k_, ideally larger than or equal to _m_, and compute the edit distance between all revisions on a page that are not more than _k_ revisions apart. This has the advantage of minimizing the amount of downloads from google cloud storage, as we must simply download the compressed block once instead of each time we need a certain revision. The _k_ value should ideally be a slightly greater than or equal to _m_. Of course, should we decide to increase _m_ at some point, the algorithm will detect a missing edit_distance and recompute it.
 
 Alternatively, we could implement a revision caching function that simply stores a number of recently pulled and nearby revisions locally. In this case, we would not prepopulate the edit_distance cache. Instead we would query the edit_distance cache, and should the edit_distance we need be missing we would query the revision cache and compute the edit distance immediately, caching it when completed.

Now, we are left with two options for how to proceed. First, we could recompute the author reputation for all authors in our environment from scratch with the addition of this new page, which we will refer to as the "clean slate" approach. This is the cleaner option, but is more computationally intensive. This would reset all author reputations to 0 and run through every revision in our environment in chronological order, recomputing the each author's reputation. This would be made significantly faster due to the edit_distance cache, as computing edit distance is by far the most computationally intensive part of the process. Alternatively, we could "patch" in this new page, simply keeping the author_reputations as they are and running the author reputation algorithms on the new page, which we will refer to as the "patch" approach. This processes the revisions out of order, and as such does not provide an exactly correct reputation, but it would hopefully provide a good approximation of reputation. Most importantly, the edit_distance cache is populated even if we patch in the page, leaving future clean slate computations much faster.

Finally, trust annotated trust would be computed live and stored statically in a CDN. This is a cost effective option, and allows us to flag a page when we determine it is out of date, and recalculate as needed.