#GaruPay

## Inspiration
The inspiration behind GaruPay comes from multiple issues we’ve all faced before — settling bills after a night out is impossible, with multiple parties each forgetful or lazy. Getting everyone in the group to pay up efficiently and accurately and tracking it also takes tremendous effort, and often gives rise to awkward conversations when somebody chases after his friend to pay up. These troubles sound so easily avoidable, and yet we haven’t encountered a hugely effective solution that truly targets the pain points surrounding inconvenience.

## Our solution
Enter GaruPay to bring all of these within reach. Our solution incorporates different parts of the above process into our everyday group chats, in the form of a Telegram Bot.

The commands will be simple and the process is intuitive and transparent. A group of friends no longer needs to go through the effort of manually calculating who owes who how much, and worse, how to settle up all the way at the end when past payments might overlap and offset one another. We also remove the need for trust in somebody to calculate everything reliably, now that we have an unbiased system to do it for them.

It is easy for users to tell the bot what they paid for and who to charge, without having to follow a rigid input structure for calculation to make sense. This is made possible by passing queries through the OpenAI LLM along with metadata surrounding it, and specifying the exact expected output format. The information is stored in our database, in something like a ledger or a dynamic debt tracker. Such flexibility of input format allows fast and easy updates to the bot anytime something needs to be tracked, while syncing well with accessibility features such as voice-to-text inputs commands.

At any time, users may ask the bot to show the current status to see how much total surplus/deficit they’re in. Finally, the bot can be asked to collate everything that’s occurred so far and output a clear table showing who pays who, and how much, to settle up all debts together.

GaruPay links well to a payment API (we used PayPal for now) then helps make the settling up payment trivial to do by instantly populating all the fields of a transfer and only requiring users to confirm they are willing to make this transfer by pressing a button on the bot. Of course, this requires a bit more setup at the start, but the payment experience becomes fast and seamless.

The root problem we want to target is convenience. Compared to previous attempts to improve peer-to-peer payment tracking, GaruPay is vastly superior in convenience through easy setup, flexible input, and quick payments.

##How we built it
Telegram, being widely used by Singaporeans, was chosen to be the user interface for best convenience. We naturally had to learn and use the Telegram API, and design its query and logic structure. To allow for flexible inputs and make sense of these texts, OpenAI was also used and integrated into the Python program structured for Telegram to query. We also used PayPal and successfully built a working payment process that seamlessly occurs with the click of a button on Telegram. MySQL was used to store session history to enable customised answers from OpenAI.

##Challenges faced
We knew Telegram was the way to go for greatest convenience, but none of us had built a Telegram Bot before. Guan Quan swiftly picked up the API, and was able to make a dummy bot within an hour. However, things got scarier as the bot required more and more features, and a few of us worked late into the night to debug and implement our vision. In the end, the GaruPay interface is successfully put into a Telegram Bot, which is nice.

OpenAI provides a developer-friendly API, which was incredible fast to learn and set up. But to integrate with the structure of our program, geared for a Telegram Bot to query, was significantly more difficult. This added to the complexity of debugging whenever the Python program behaves unexpectedly.

Finally, we wanted to use a more local and commonly-used payment system like PayPal or PayNow, but these were not developer-friendly and required too much administrative work to set up. Instead, we opted to use PayPal which provides intuitive developer docs, API, and even a sandbox environment to try things out. The implementation details created countless roadblocks along the way, including problems with authorization headers and account keys, which cost us many more hours to figure out.

In the end, we successfully learnt many skills and technologies, and created a working MVP that depicts the flow of our idea reasonably well. Unfortunately, some parts are not ironed out as we picked our battles under a strict time limit, but they’re possible for future development.
