Analysis
========

The website will contain general information, such as tutorials, blogs etc. for learning and entertainment as well as critical information, that need to be updated quickly and easily, such as results of competitions etc. 

The website will mainly be informative, as opposed to being interactive. However, in the future, we might want bit more interactive functionality, such as registration forms, polls, short quizzes etc. Thus, the possibility of adding interactive functionality in the backend needs to be open.

Since website does not need any **complex functionality**, its best to use a **Content Management System**.

Wordpress, Joomla, Drupal, SquareSpace etc. are all popular, but lack in one aspect - There is little or no scope of adding **complex functionality** later on. By complex functionality, we refer to **logical constructs** in the backend. **Moreover, they are not free**.

We do not need any functionality now, but we would like to keep our options open for the future. To allow for future scalability in terms of functionality and features, we chose to go for python or django based CMS. **Python** is easy to learn for even beginners. It's also super popular language today. **Django** as a web framework has its ups and downs, but for the most part - it works beautifully. The beauty lies in its strong `design philosophy <https://docs.djangoproject.com/en/2.0/misc/design-philosophies/>`_

There are several django based content management systems - most popular being **Django-CMS**, **Wagtail** and **Mezzanine**. Each have their pros and cons. But the flexibility of Stream Field in Wagtail is unparalled. For more details, `listen to Adam <https://www.youtube.com/watch?v=3UC1MNFOjEI>`_. That made us choose `Wagtail <https://wagtail.io/>`_ over the other two. 
