// ************************************************************************** //
//                                                                            //
//                                                        :::      ::::::::   //
//   status.rs                                          :+:      :+:    :+:   //
//                                                    +:+ +:+         +:+     //
//   By: dfine <coding@dfine.tech>                  +#+  +:+       +#+        //
//                                                +#+#+#+#+#+   +#+           //
//   Created: 2025/03/20 20:10:01 by dfine             #+#    #+#             //
//   Updated: 2025/03/20 20:10:01 by dfine            ###   ########.fr       //
//                                                                            //
// ************************************************************************** //

use actix_web::{HttpResponse, Responder, Scope, get, web};

#[get("")]
async fn status() -> impl Responder {
    HttpResponse::Ok().body("AI GAME CREATOR!")
}

pub fn routes() -> Scope {
    web::scope("/status").service(status)
}
