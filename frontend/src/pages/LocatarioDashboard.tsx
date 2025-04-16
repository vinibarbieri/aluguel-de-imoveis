import { useEffect, useState } from "react";
import axios from "axios";
import GooglePlacesAutocomplete from "react-google-places-autocomplete";
import { getLoggedUser, logout } from "../utils/auth";

interface Property {
  id: number;
  title: string;
  description: string;
  address: string;
  price_per_day: number;
  available_from: string;
  available_until: string;
  average_rating: number | null;
  image_url?: string;
}

interface Reservation {
  reservation_id: number;
  property_id: number;
  property_title: string;
  image_url?: string;
  start_date: string;
  end_date: string;
  approved: boolean | null;
  review?: {
    rating: number;
    comment: string;
  };
}

export default function LocatarioDashboard() {
  const user = getLoggedUser();
  const [tab, setTab] = useState<"buscar" | "reservas">("buscar");

  const [searchCity, setSearchCity] = useState<string>("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [results, setResults] = useState<Property[]>([]);
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [reviews, setReviews] = useState<Record<number, { rating: number; comment: string }>>({});

  useEffect(() => {
    if (tab === "reservas") {
      loadReservations();
    }
  }, [tab]);

  const loadReservations = async () => {
    const res = await axios.get(`http://localhost:5000/api/locatario/my-reservations/${user.id}`);
    setReservations(res.data);
  };

  const handleSearch = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/locatario/search", {
        params: {
          city: searchCity,
          min_price: minPrice || 0,
          max_price: maxPrice || 999999,
          start_date: startDate,
          end_date: endDate,
        },
      });
      setResults(res.data);
    } catch (err) {
      alert("Erro ao buscar imóveis.");
    }
  };

  const handleReserve = async (propertyId: number) => {
    try {
      if (!startDate || !endDate) {
        alert("Selecione as datas antes de reservar.");
        return;
      }

      console.log(propertyId)

      await axios.post("http://localhost:5000/api/locatario/reserve", {
        property_id: propertyId,
        renter_id: user.id,
        start_date: startDate,
        end_date: endDate,
      });

      alert("Reserva solicitada com sucesso!");
    } catch (err: any) {
      alert(err.response?.data?.error || "Erro ao reservar imóvel.");
    }
  };

  const handleReviewSubmit = async (reservation_id: number) => {
    const review = reviews[reservation_id];
    if (!review || !review.rating || !review.comment) {
      alert("Preencha nota e comentário.");
      return;
    }

    try {
      await axios.post("http://localhost:5000/api/locatario/review", {
        reservation_id,
        rating: review.rating,
        comment: review.comment,
      });

      alert("Avaliação enviada com sucesso!");
      loadReservations();
    } catch (err) {
      alert("Erro ao enviar avaliação.");
    }
  };

  const futureReservations = reservations.filter((r) => new Date(r.end_date) > new Date());
  const pastReservations = reservations.filter(r => new Date(r.end_date) < new Date());

  return (
    <div className="container mt-4">
      <h2>Olá, {user.name}</h2>
      <button className="btn btn-outline-danger float-end" onClick={logout}>
        Sair
      </button>

      <ul className="nav nav-tabs mt-4">
        <li className="nav-item">
          <button className={`nav-link ${tab === "buscar" ? "active" : ""}`} onClick={() => setTab("buscar")}>
            Buscar Imóveis
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${tab === "reservas" ? "active" : ""}`} onClick={() => setTab("reservas")}>
            Minhas Reservas
          </button>
        </li>
      </ul>



      <div className="mt-4">
        {tab === "buscar" && (
          <>
            <h4>Buscar imóveis</h4>
            <GooglePlacesAutocomplete
              apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
              selectProps={{
                placeholder: "Digite a cidade ou bairro...",
                onChange: (value: any) => {
                  setSearchCity(value.label);
                },
              }}
            />

            <div className="row mt-3">
              <div className="col-md-3">
                <input className="form-control mb-2" placeholder="Preço mínimo" type="number" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} />
              </div>
              <div className="col-md-3">
                <input className="form-control mb-2" placeholder="Preço máximo" type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
              </div>
              <div className="col-md-3">
                <input className="form-control mb-2" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
              </div>
              <div className="col-md-3">
                <input className="form-control mb-2" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
              </div>
            </div>

            <button className="btn btn-primary" onClick={handleSearch}>
              Buscar
            </button>

            <div className="mt-4">
              <h4>Resultados</h4>
              {results.length === 0 && <p>Nenhum imóvel encontrado.</p>}
              {results.map((p) => (
                <div key={p.id} className="card mb-3">
                  {p.image_url && <img src={p.image_url} alt="" className="card-img-top" style={{ maxHeight: "200px", objectFit: "cover" }} />}
                  <div className="card-body">
                    <h5 className="card-title">{p.title}</h5>
                    <p>{p.description}</p>
                    <p className="text-muted">{p.address}</p>
                    <p>
                      💵 R${p.price_per_day} | Disponível de {p.available_from} até {p.available_until}
                    </p>
                    {p.average_rating !== null && <p>⭐ {p.average_rating} / 5</p>}
                    <button className="btn btn-success" onClick={() => handleReserve(p.id)}>
                      Reservar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {tab === "reservas" && (
          <>
            <h4>📅 Reservas Futuras</h4>
            {futureReservations.length === 0 && <p>Nenhuma reserva futura.</p>}
            {futureReservations.map((r) => (
              <div key={r.reservation_id} className="card mb-3">
                {r.image_url && <img src={r.image_url} alt="" className="card-img-top" style={{ maxHeight: "200px", objectFit: "cover" }} />}
                <div className="card-body">
                  <h5>{r.property_title}</h5>
                  <p>De {r.start_date} até {r.end_date}</p>
                  <p>Status: {r.approved === null ? "Pendente" : r.approved ? "Aprovada" : "Recusada"}</p>
                </div>
              </div>
            ))}

            <h4 className="mt-4">✅ Reservas Concluídas</h4>
            {pastReservations.length === 0 && <p>Nenhuma reserva passada.</p>}
            {pastReservations.map((r) => (
              <div key={r.reservation_id} className="card mb-3">
                {r.image_url && <img src={r.image_url} alt="" className="card-img-top" style={{ maxHeight: "200px", objectFit: "cover" }} />}
                <div className="card-body">
                  <h5>{r.property_title}</h5>
                  <p>De {r.start_date} até {r.end_date}</p>
                  <p>Status: {r.approved === null ? "Pendente" : r.approved ? "Aprovada" : "Recusada"}</p>

                  {/* Se ainda não avaliou e foi aprovada */}
                  {r.approved && !r.review && (
                    <>
                      <h6 className="mt-3">Avaliar imóvel:</h6>
                      <input
                        className="form-control mb-2"
                        placeholder="Nota (1 a 5)"
                        type="number"
                        min={1}
                        max={5}
                        onChange={(e) =>
                          setReviews({ ...reviews, [r.reservation_id]: { ...reviews[r.reservation_id], rating: Number(e.target.value) } })
                        }
                      />
                      <textarea
                        className="form-control mb-2"
                        placeholder="Comentário"
                        onChange={(e) =>
                          setReviews({ ...reviews, [r.reservation_id]: { ...reviews[r.reservation_id], comment: e.target.value } })
                        }
                      />
                      <button className="btn btn-primary" onClick={() => handleReviewSubmit(r.reservation_id)}>
                        Enviar Avaliação
                      </button>
                    </>
                  )}

                  {r.review && (
                    <>
                      <p className="mt-2"><strong>Sua avaliação:</strong></p>
                      <p>⭐ {r.review.rating}</p>
                      <p>{r.review.comment}</p>
                    </>
                  )}
                </div>
              </div>
            ))}
          </>
        )}
        </div>
      </div>
    );
  }